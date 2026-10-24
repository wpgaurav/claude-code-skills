#!/usr/bin/env bash
# Validate every skill folder: frontmatter, link targets, private-path gate, scripts, tests.

set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"

fail=0
say() { printf '%s\n' "$*" >&2; fail=1; }

for required in README.md LICENSE LICENSE-APACHE-2.0 NOTICE.md CONTRIBUTING.md CHANGELOG.md install.sh; do
  [[ -s "$required" ]] || say "Missing or empty: $required"
done

python3 - <<'EOF' || fail=1
import re, sys, pathlib
root = pathlib.Path('.')
bad = 0
for skill_dir in sorted(p for p in root.iterdir() if p.is_dir() and (p / 'SKILL.md').is_file()):
    text = (skill_dir / 'SKILL.md').read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        print(f"{skill_dir}: SKILL.md must start with YAML frontmatter"); bad += 1; continue
    end = text.find('\n---\n', 4)
    fm, body = text[4:end], text[end + 5:]
    name = re.search(r'^name:\s*(\S+)\s*$', fm, re.M)
    if not name or name.group(1) != skill_dir.name:
        print(f"{skill_dir}: frontmatter name must equal the folder name"); bad += 1
    if name and not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name.group(1)) or (name and len(name.group(1)) > 64):
        print(f"{skill_dir}: name must be lowercase letters, digits, hyphens, max 64 chars"); bad += 1
    desc = re.search(r'^description:\s*(.*?)(?=^\S|\Z)', fm, re.M | re.S)
    desc_text = ' '.join(desc.group(1).split()) if desc else ''
    if not desc_text:
        print(f"{skill_dir}: description is required"); bad += 1
    elif len(desc_text) > 1024:
        print(f"{skill_dir}: description is {len(desc_text)} chars; the Agent Skills spec caps it at 1024"); bad += 1
    if not re.search(r'^license:', fm, re.M):
        print(f"{skill_dir}: license field is required"); bad += 1
    if 'user-invokable' in fm:
        print(f"{skill_dir}: 'user-invokable' is not a Claude Code key (it is 'user-invocable'); remove it"); bad += 1
    if re.search(r'^args:', fm, re.M):
        print(f"{skill_dir}: 'args' is not a documented frontmatter key; use argument-hint or arguments"); bad += 1
    for link in re.findall(r'\]\((?!https?://|#|mailto:)([^)]+)\)', body):
        target = (skill_dir / link.split('#')[0]).resolve()
        if not target.exists():
            print(f"{skill_dir}: broken relative link {link}"); bad += 1
    for f in skill_dir.rglob('*'):
        if f.name.startswith('local-'):
            print(f"{f}: local-only file; it must never be published"); bad += 1
        if f.is_file() and f.suffix in ('.md', '.json', '.py', '.sh', '.txt'):
            content = f.read_text(encoding='utf-8', errors='replace')
            if re.search(r'(/Users/|~/\.env|cookies\.json|gho_[A-Za-z0-9]|github_pat_|claude-sync|Mobile Documents|writing-system/|local-only:(?:start|end)|anti-slop/|\bquality/quality-gates)', content):
                print(f"{f}: contains a private path or credential-like value"); bad += 1
print(f"checked {sum(1 for p in root.iterdir() if p.is_dir() and (p / 'SKILL.md').is_file())} skills")
sys.exit(1 if bad else 0)
EOF

for py in $(find . -name '*.py' -not -path './.git/*'); do
  python3 -m py_compile "$py" || say "py_compile failed: $py"
done

python3 -c 'import json,sys; json.load(open("slop-detector/slop-detector.json"))' || say "slop-detector.json is not valid JSON"
python3 slop-detector/scripts/test-severity.py >/dev/null || say "slop-detector regression tests failed"

bash -n install.sh || say "install.sh has a syntax error"

if [[ $fail -ne 0 ]]; then
  echo "Validation failed." >&2
  exit 1
fi
echo "Validation passed."
