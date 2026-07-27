#!/usr/bin/env bash
# Operator helper: create M1–M4 milestones, labels, and DRL-001..030 issues.
# Requires authenticated gh with repo write access. Safe to re-run for labels;
# milestone/issue creation should be reviewed before duplicate filing.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI required" >&2
  exit 1
fi

echo "Creating labels from .github/labels.yml (best-effort)..."
python3 - <<'PY'
import subprocess, sys, yaml
from pathlib import Path
data = yaml.safe_load(Path('.github/labels.yml').read_text())
for label in data['labels']:
    cmd = [
        'gh', 'label', 'create', label['name'],
        '--color', label['color'],
        '--description', label.get('description', ''),
        '--force',
    ]
    subprocess.run(cmd, check=False)
print('labels synced')
PY

echo "Creating milestones..."
python3 - <<'PY'
import subprocess, yaml
from pathlib import Path
ms = yaml.safe_load(Path('.github/milestones.yml').read_text())['milestones']
for m in ms:
    title = m['title']
    body = m.get('description', '')
    # create if missing
    existing = subprocess.check_output(['gh', 'api', 'repos/{owner}/{repo}/milestones'], text=True)
    if title in existing:
        print('exists', title)
        continue
    subprocess.run([
        'gh', 'api', 'repos/{owner}/{repo}/milestones', '-f', f'title={title}', '-f', f'description={body}'
    ], check=False)
print('milestones done')
PY

echo "Filing issues from requirements/issue-register.yaml ..."
python3 - <<'PY'
import subprocess, yaml
from pathlib import Path
reg = yaml.safe_load(Path('requirements/issue-register.yaml').read_text())
# map milestone id to title
ms = {m['id']: m['title'] for m in reg['milestones']}
for issue in reg['issues']:
    body_path = Path(issue['body'])
    title = f"{issue['id']}: {issue['title']}"
    labels = ','.join(issue['labels'])
    milestone = ms[issue['milestone']]
    body = body_path.read_text()
    # skip if issue title already exists
    found = subprocess.run(
        ['gh', 'issue', 'list', '--search', f'in:title {issue["id"]}', '--json', 'number,title'],
        capture_output=True, text=True, check=False,
    )
    if issue['id'] in (found.stdout or ''):
        print('skip existing', issue['id'])
        continue
    subprocess.run([
        'gh', 'issue', 'create',
        '--title', title,
        '--body', body,
        '--label', labels,
        '--milestone', milestone,
    ], check=False)
    print('filed', issue['id'])
print('done')
PY

echo "Review created issues before assigning. Prefer filing DRL-001–006 first."
