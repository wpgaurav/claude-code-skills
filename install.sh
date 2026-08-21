#!/usr/bin/env bash
# Install one or more skills from this repository into an agent's skills directory.
#
#   ./install.sh claude                     # all skills -> ~/.claude/skills/
#   ./install.sh claude stop-slop red-pen   # only these
#   ./install.sh codex                      # ~/.codex/skills/
#   ./install.sh cursor                     # ~/.cursor/skills/
#
# Set SKILLS_INSTALL_DIR to override the destination directory.

set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target="${1:-}"

case "$target" in
  claude) default_dir="${HOME}/.claude/skills" ;;
  codex)  default_dir="${HOME}/.codex/skills" ;;
  cursor) default_dir="${HOME}/.cursor/skills" ;;
  -h|--help|"")
    sed -n '2,9p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
    exit 0
    ;;
  *)
    echo "Unknown target: ${target}. Use claude, codex, or cursor." >&2
    exit 1
    ;;
esac
shift

install_dir="${SKILLS_INSTALL_DIR:-$default_dir}"

all_skills=()
for dir in "$repo_dir"/*/; do
  [[ -f "${dir}SKILL.md" ]] && all_skills+=("$(basename "$dir")")
done

if [[ $# -gt 0 ]]; then
  skills=("$@")
else
  skills=("${all_skills[@]}")
fi

mkdir -p "$install_dir"

for skill in "${skills[@]}"; do
  src="${repo_dir}/${skill}"
  if [[ ! -f "${src}/SKILL.md" ]]; then
    echo "No such skill in this repository: ${skill}" >&2
    echo "Available: ${all_skills[*]}" >&2
    exit 1
  fi
  dest="${install_dir}/${skill}"
  if [[ "$dest" == "$src" ]]; then
    echo "${skill}: already at ${dest}"
    continue
  fi
  rm -rf "$dest"
  mkdir -p "$dest"
  (cd "$src" && find . -type f ! -name '.DS_Store' ! -path '*/__pycache__/*' -print0) \
    | (cd "$src" && xargs -0 -I{} sh -c 'mkdir -p "$1/$(dirname "$2")" && cp "$2" "$1/$2"' _ "$dest" {})
  echo "${skill}: installed at ${dest}"
done

echo "Done. Restart your agent so it discovers the new skills."
