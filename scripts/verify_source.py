"""Fail on unexpected tracked paths, raw-data file types or credential signatures."""
from pathlib import Path
import re
from subprocess import check_output

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_DIRS = (".github/", "docs/", "patient_outreach/", "research/", "scripts/", "tests/", "web/")
ALLOWED_ROOT = {
    "AGENTS.md", "CLAUDE.md", "MASTER_PROMPT.md", "CONTINUATION_V1.md", "PLANS.md", "progress.md", "PROJECT_STATE.json",
    "DECISIONS.md", "FINAL_COMPLETION.md", "CHANGELOG.md", "README.md", "LICENSE", ".gitignore", ".gitattributes",
    "pyproject.toml", "uv.lock",
}
DENIED_PREFIXES = ("data/", "research/source-inputs/", "web/dist/", "web/qa-output/", ".wrangler/")
DENIED_SUFFIXES = {
    ".parquet", ".csv", ".tsv", ".dta", ".tab", ".do", ".pkl", ".joblib", ".zip", ".pdf", ".docx", ".xlsx",
    ".pem", ".key", ".env", ".map", ".pyc", ".gguf", ".safetensors",
}
CREDENTIAL = re.compile(
    rb"(?:gh[pousr]_|github_pat_|sk-proj-|xox[baprs]-)[A-Za-z0-9_-]{15,}"
    rb"|\b(?:AKIA|ASIA)[A-Z0-9]{16}\b|-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----"
)


def main() -> None:
    files = check_output(["git", "ls-files", "--stage", "-z"], cwd=ROOT).split(b"\0")
    entries = [entry.decode().split("\t", 1) for entry in files if entry]
    for metadata, name in entries:
        mode, digest, stage = metadata.split()
        path = ROOT / name
        if (mode not in {"100644", "100755"} or stage != "0" or name.startswith(DENIED_PREFIXES)
                or path.suffix.lower() in DENIED_SUFFIXES or "node_modules" in path.parts
                or not (name in ALLOWED_ROOT or name.startswith(ALLOWED_DIRS))):
            raise SystemExit("Unsafe tracked path: " + name)
        staged = check_output(["git", "cat-file", "blob", digest], cwd=ROOT)
        if CREDENTIAL.search(staged):
            raise SystemExit("Credential pattern in tracked file: " + name)
    print(f"Verified {len(entries)} staged source paths.")


if __name__ == "__main__":
    main()
