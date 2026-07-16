#!/usr/bin/env bash
# claude-kit installer — copies skills, agents and commands into ~/.claude
# Existing files are never overwritten; they are reported as skipped.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_HOME:-$HOME/.claude}"

installed=0
skipped=0
skipped_names=()

install_dir() {
  local kind="$1"       # skills | agents | commands
  local src="$SRC/$kind"
  local dest="$DEST/$kind"

  [ -d "$src" ] || return 0
  mkdir -p "$dest"

  local entry name
  for entry in "$src"/*; do
    [ -e "$entry" ] || continue
    name="$(basename "$entry")"
    if [ -e "$dest/$name" ]; then
      skipped=$((skipped + 1))
      skipped_names+=("$kind/$name")
      continue
    fi
    cp -R "$entry" "$dest/$name"
    installed=$((installed + 1))
  done
}

echo "claude-kit → $DEST"
echo

install_dir skills
install_dir agents
install_dir commands

echo "Installed: $installed"
echo "Skipped (already present): $skipped"

if [ "$skipped" -gt 0 ]; then
  echo
  echo "Skipped items — remove them yourself first if you want this version:"
  printf '  %s\n' "${skipped_names[@]}"
fi

echo
echo "Restart Claude Code to pick up the new skills and agents."
