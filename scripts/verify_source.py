"""Fail on unexpected tracked paths, raw-data file types or credential signatures."""
from pathlib import Path
import re
from subprocess import check_output

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_DIRS = (".github/", "docs/", "patient_outreach/", "research/", "scripts/", "tests/", "web/")
ALLOWED_ROOT = {
    "AGENTS.md", "CLAUDE.md", "MASTER_PROMPT.md", "PLANS.md", "progress.md", "PROJECT_STATE.json",
    "DECISIONS.md", "CHANGELOG.md", "README.md", "LICENSE", ".gitignore", ".gitattributes",
    "pyproject.toml", "uv.lock",
}
DENIED_PREFIXES = ("data/", "research/source-inputs/", "web/dist/", "web/qa-output/", ".wrangler/")
DENIED_SUFFIXES = {".parquet",".csv",".pkl",".joblib",".zip",".docx",".pem",".key",".env",".map",".pyc"}
CREDENTIAL = re.compile(rb"(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_-]{15,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")


def main() -> None:
    paths = [name.decode() for name in check_output(["git","ls-files","-z"], cwd=ROOT).split(b"\0") if name]
    for name in paths:
        path = ROOT / name
        if (name.startswith(DENIED_PREFIXES) or path.suffix.lower() in DENIED_SUFFIXES
                or "node_modules" in path.parts or path.is_symlink()
                or not (name in ALLOWED_ROOT or name.startswith(ALLOWED_DIRS))):
            raise SystemExit("Unsafe tracked path: " + name)
        staged = check_output(["git","show",":"+name],cwd=ROOT)
        if CREDENTIAL.search(staged):
            raise SystemExit("Credential pattern in tracked file: " + name)
    print(f"Verified {len(paths)} staged source paths.")


if __name__ == "__main__":
    main()
