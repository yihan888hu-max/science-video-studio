"""Check repository text, declared media, file integrity and local path leakage."""
import argparse, ast, hashlib, json, re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
project = root / "projects/survivorship-bias"
p = argparse.ArgumentParser()
p.add_argument("--require-assets", action="store_true")
args = p.parse_args()
errors = []
manifest_file = root / "FILE_MANIFEST.json"
if not manifest_file.exists():
    raise SystemExit("FILE_MANIFEST.json is required")
entries = json.loads(manifest_file.read_text(encoding="utf-8"))["files"]
for entry in entries:
    path = (root / entry["path"]).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        errors.append("Missing or unsafe file: " + entry["path"])
        continue
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != entry["sha256"]:
        errors.append("Changed reviewed file: " + entry["path"])
    if path.suffix in {".py", ".json", ".md", ".html", ".svg"}:
        content = data.decode("utf-8-sig")
        if path.suffix == ".py":
            ast.parse(content, filename=entry["path"])
        elif path.suffix == ".json":
            json.loads(content)
        if re.search(r"(?:C:[/\\]Users[/\\]|E:[/\\])", content, flags=re.I):
            errors.append("Machine-specific path: " + entry["path"])
        if re.search(r"gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----", content):
            errors.append("Potential credential: " + entry["path"])
assets = json.loads((project / "local-assets.example.json").read_text(encoding="utf-8"))["assets"]
missing = []
for asset in assets:
    path = project / asset["path"]
    if not path.is_file():
        missing.append(asset["path"])
    elif hashlib.sha256(path.read_bytes()).hexdigest() != asset["sha256"]:
        errors.append("Asset hash mismatch: " + asset["path"])
    if ("projects/survivorship-bias/" + asset["path"]) in {e["path"] for e in entries}:
        errors.append("Local asset incorrectly tracked")
if args.require_assets and missing:
    errors.append("Missing local assets: " + ", ".join(missing))
report = {"ok": not errors, "reviewed_files": len(entries), "declared_assets": len(assets),
          "local_assets_present": len(assets)-len(missing), "require_assets": args.require_assets,
          "errors": errors, "github_uploaded": False,
          "scope": "Source/package validation; no fresh render or subjective AV review claimed"}
(root / "validation-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(0 if report["ok"] else 1)
