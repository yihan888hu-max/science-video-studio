"""Record exactly the staged Git snapshot, excluding self-referential reports."""
import hashlib
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
text_suffixes = {'.py', '.json', '.md', '.html', '.svg', '.ts', '.tsx', '.mjs', '.yaml', '.yml', '.csv', '.js', '.css', '.txt'}
records = subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=root).split(b'\0')
entries = []
for record in records:
    if not record:
        continue
    header, path = record.split(b'\t', 1)
    mode, sha, stage = header.split()
    path = path.decode('utf-8')
    if path in ('FILE_MANIFEST.json', 'validation-report.json'):
        continue
    if stage != b'0' or mode not in (b'100644', b'100755'):
        raise SystemExit('Unmerged or unsupported entry: ' + path)
    data = subprocess.check_output(['git', 'cat-file', 'blob', sha.decode()], cwd=root)
    # Preserve inherited blobs while giving CRLF/LF checkouts the same text
    # checksum. New files are checked in with LF through .gitattributes.
    if Path(path).suffix in text_suffixes or Path(path).name in {'.gitignore', '.gitattributes', '.prettierrc'}:
        data = data.replace(b'\r\n', b'\n')
    entries.append(dict(path=path, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
manifest = dict(scope='Staged source, production records and versioned synchronized previews; private raw media, dependencies and caches excluded',
                textLineEndings='Canonical LF checksums for text, including inherited CRLF blobs; binary files byte-exact', files=entries)
(root/'FILE_MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print('Recorded staged files:', len(entries))
