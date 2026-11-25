"""Verify public file metadata, or retrieve pinned files after documented approval."""
import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from time import sleep
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, build_opener
from zipfile import ZipFile

BASE = "https://files.osf.io/v1/resources/mqbux/providers/osfstorage"
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MANIFEST = ROOT / "research" / "manifests" / "osf_mqbux_manifest.json"


@dataclass(frozen=True)
class Entry:
    study: int
    name: str
    remote: str
    member: str
    size: int
    sha256: str


def load_manifest(path: Path = MANIFEST) -> list[Entry]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["node"] != "mqbux" or data["waterbutler_base"] != BASE:
        raise ValueError("Unexpected manifest source.")
    result = []
    seen_targets = set()
    seen_ids = set()
    for raw in data["files"]:
        member = raw["materialized"]
        parts = member.split("/")[1:]
        name = parts[-1]
        if (not member.startswith("/") or any(part in ("", ".", "..") for part in parts)
                or any(c in member for c in ("\\", ":", "\x00"))
                or not re.fullmatch(r"[a-zA-Z0-9_.-]+\.(csv|txt)", name)
                or not re.fullmatch(r"/[a-f0-9]{24}", raw["osf_path"])
                or not re.fullmatch(r"[a-f0-9]{64}", raw["sha256"])
                or type(raw["study"]) is not int or not 1 <= raw["study"] <= 4
                or type(raw["size"]) is not int or not 0 < raw["size"] <= 250_000_000):
            raise ValueError("Unsafe pinned manifest entry.")
        target = (raw["study"], name.casefold())
        if target in seen_targets or raw["osf_path"] in seen_ids:
            raise ValueError("Duplicate pinned file.")
        seen_targets.add(target)
        seen_ids.add(raw["osf_path"])
        result.append(Entry(raw["study"], name, raw["osf_path"], member.lstrip("/"),
                            raw["size"], raw["sha256"]))
    if not result:
        raise ValueError("Empty manifest.")
    return result


class HttpsRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        url = urlparse(newurl)
        host = url.hostname or ""
        if url.scheme != "https" or url.username or url.password or url.port not in (None, 443) or not (
            host in ("files.osf.io", "api.osf.io", "osf.io", "storage.googleapis.com")
            or host.endswith(".osf.io") or host.endswith(".amazonaws.com")
        ):
            raise ValueError("Blocked unexpected OSF redirect.")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def retry(operation):
    for attempt in range(3):
        try:
            return operation()
        except (URLError, TimeoutError, ConnectionError) as error:
            if isinstance(error, HTTPError) and error.code not in (429, 500, 502, 503, 504):
                raise
            if attempt == 2:
                raise
            sleep(2**attempt)
    raise AssertionError("Unreachable retry state.")


def verify_metadata(entries: list[Entry]) -> dict:
    opener = build_opener(HttpsRedirect())
    results = []
    for entry in entries:
        def read():
            url = "https://api.osf.io/v2/files" + entry.remote + "/"
            with opener.open(url, timeout=20) as response:
                return json.load(response)["data"]["attributes"]
        try:
            metadata = retry(read)
            size = metadata.get("size")
            checksum = metadata.get("extra", {}).get("hashes", {}).get("sha256")
            matches = (metadata.get("name"), size, checksum) == (entry.name, entry.size, entry.sha256)
            result = {"status": "match" if matches else "mismatch", "size": size, "sha256": checksum}
        except (OSError, KeyError, ValueError) as error:
            result = {"status": "unavailable", "error_type": type(error).__name__,
                      "http_status": getattr(error, "code", None)}
        results.append({"study": entry.study, "name": entry.name, **result})
    return {"source": "https://api.osf.io/v2/files/", "verification": "metadata_only", "files": results}


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def quarantine(path: Path, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    if directory.is_symlink() or directory.is_junction():
        raise ValueError("Quarantine must be a literal directory.")
    with NamedTemporaryFile(dir=directory, prefix=path.name + "-", suffix=".quarantine", delete=False) as handle:
        destination = Path(handle.name)
    path.replace(destination)


def receive(entry: Entry, source, target: Path) -> None:
    h = hashlib.sha256()
    size = 0
    with NamedTemporaryFile(dir=target.parent, suffix=".part", delete=False) as handle:
        temp = Path(handle.name)
        try:
            while chunk := source.read(min(65536, max(1, entry.size + 1 - size))):
                handle.write(chunk)
                size += len(chunk)
                h.update(chunk)
                if size > entry.size:
                    break
        except BaseException:
            handle.close()
            temp.unlink(missing_ok=True)
            raise
    if size != entry.size or h.hexdigest() != entry.sha256:
        quarantine(temp, target.parent / "quarantine")
        raise ValueError(f"{entry.name}: size or SHA-256 mismatch, quarantined.")
    temp.replace(target)


def acquire(entries: list[Entry], archive: ZipFile | None = None) -> None:
    # Never derive a filesystem path from an archive member. Only consume exact pinned entries.
    paths = [RAW.parent, RAW]
    for path in paths:
        if path.is_symlink() or path.is_junction():
            raise ValueError("Restricted storage must be a literal project directory.")
    opener = build_opener(HttpsRedirect())
    members = {}
    if archive:
        for item in archive.infolist():
            if item.filename in members:
                raise ValueError("Duplicate member in supplied archive.")
            members[item.filename] = item
    for entry in entries:
        folder = RAW / f"study{entry.study}"
        if folder.is_symlink() or folder.is_junction():
            raise ValueError("Study path must be a literal directory.")
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / entry.name
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError("Unexpected target type.")
        if target.exists():
            if target.stat().st_size == entry.size and digest(target) == entry.sha256:
                continue
            quarantine(target, folder / "quarantine")
            raise ValueError(f"{entry.name}: existing local file mismatched the manifest and was quarantined.")
        if archive:
            info = members.get(entry.member)
            if info is None or info.is_dir() or info.file_size != entry.size or (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError(f"{entry.name}: exact pinned archive member unavailable.")
            with archive.open(info) as stream:
                receive(entry, stream, target)
        else:
            def download():
                with opener.open(BASE + entry.remote, timeout=30) as stream:
                    receive(entry, stream, target)
            retry(download)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--approved-rights-record", type=Path)
    args = parser.parse_args()
    entries = load_manifest()
    if args.download or args.archive:
        record = args.approved_rights_record
        if not record or not record.is_file():
            parser.error("Retrieval requires independently documented permission for the intended use.")
        approval = json.loads(record.read_text(encoding="utf-8"))
        if (approval.get("node") != "mqbux" or approval.get("analysis_approved") is not True
                or not isinstance(approval.get("basis"), str) or not approval["basis"].strip()):
            parser.error("Invalid documented analysis permission.")
        if args.archive:
            with ZipFile(args.archive) as archive:
                acquire(entries, archive)
        else:
            acquire(entries)
        print(f"All {len(entries)} pinned payloads verified.")
    else:
        report = verify_metadata(entries)
        print(json.dumps(report, indent=2))
        if any(record["status"] != "match" for record in report["files"]):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
