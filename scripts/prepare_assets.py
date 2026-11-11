"""Restore the exact allowlisted local assets; never fetch or overwrite different files."""
import argparse, hashlib, json, shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
project = root / "projects/survivorship-bias"
parser = argparse.ArgumentParser()
parser.add_argument("--from-project", type=Path, required=True)
parser.add_argument("--dry-run", action="store_true")
args = parser.parse_args()
source_root = args.from_project.resolve()
manifest = json.loads((project / "local-assets.example.json").read_text(encoding="utf-8"))
plan = []
for asset in manifest["assets"]:
    rel = Path(asset["path"])
    source = (source_root / rel).resolve()
    target = (project / rel).resolve()
    if rel.is_absolute() or not source.is_relative_to(source_root) or not target.is_relative_to(project.resolve()):
        raise SystemExit("Asset path escapes the selected project")
    if not source.is_file():
        raise SystemExit("Missing source asset: " + rel.as_posix())
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != asset["sha256"] or source.stat().st_size != asset["bytes"]:
        raise SystemExit("Source asset differs from reviewed manifest: " + rel.as_posix())
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        raise SystemExit("Refusing to overwrite a different local asset: " + rel.as_posix())
    plan.append((source, target, rel))
for source, target, rel in plan:
    if not args.dry_run and not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    print(("CHECK " if args.dry_run else "READY ") + rel.as_posix())
print("Validated assets:", len(plan))
