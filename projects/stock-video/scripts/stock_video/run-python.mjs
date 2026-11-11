import {spawnSync} from 'node:child_process';
const args = process.argv.slice(2);
const candidates = process.platform === 'win32'
  ? [['py', '-3'], ['python'], ['python3']]
  : [['python3'], ['python']];
for (const [cmd, ...prefix] of candidates) {
  const probe = spawnSync(cmd, [...prefix, '--version'], {encoding: 'utf8', timeout: 5000});
  if (probe.status !== 0 || !/^Python 3\./.test((probe.stdout || '') + (probe.stderr || ''))) continue;
  const result = spawnSync(cmd, [...prefix, ...args], {stdio: 'inherit', env: {...process.env, PYTHONUTF8: '1'}});
  if (result.error) console.error(result.error.message);
  process.exit(result.status ?? 1);
}
console.error('Python 3 is required. Install it from python.org, then retry.');
process.exit(1);
