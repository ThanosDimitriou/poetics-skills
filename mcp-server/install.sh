#!/usr/bin/env bash
# Poetics brand MCP server — one-command installer.
#
# Handles the editors that DON'T support workspace-scoped MCP config (i.e.
# don't read a .mcp.json/mcp.json shipped in the repo): Claude Desktop and
# Windsurf. VS Code, Cursor, and Claude Code already auto-configure from
# .vscode/mcp.json, .cursor/mcp.json, and .mcp.json the moment you open this
# repo — nothing to run for those.
#
# Usage:
#   bash mcp-server/install.sh
#
# Safe to re-run: only ever adds/updates the "poetics-brand" entry in each
# config file; every other entry (other MCP servers you have configured) is
# left untouched, and a .bak backup is written before any change.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$HERE")"
SERVER_PATH="$HERE/server.py"

echo "Poetics brand MCP server installer"
echo "Repo: $REPO_ROOT"
echo

# -- Find a Python 3.10+ interpreter -------------------------------------------
PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$candidate" >/dev/null 2>&1; then
    ver="$("$candidate" -c 'import sys; print(sys.version_info[:2])' 2>/dev/null || echo "(0, 0)")"
    major=$(echo "$ver" | tr -dc '0-9,' | cut -d',' -f1)
    minor=$(echo "$ver" | tr -dc '0-9,' | cut -d',' -f2)
    if [ "${major:-0}" -eq 3 ] && [ "${minor:-0}" -ge 10 ]; then
      PYTHON="$candidate"
      break
    fi
  fi
done

if [ -z "$PYTHON" ]; then
  echo "ERROR: no Python 3.10+ found. The MCP SDK requires it."
  echo "Install one (e.g. 'brew install python@3.11' on macOS) and re-run this script."
  exit 1
fi
echo "Using: $($PYTHON --version) at $(command -v "$PYTHON")"

# -- Install the MCP SDK ---------------------------------------------------------
echo "Installing dependencies..."
"$PYTHON" -m pip install -q -r "$HERE/requirements.txt" \
  || "$PYTHON" -m pip install -q --break-system-packages -r "$HERE/requirements.txt"

# -- Configure Claude Desktop (global config, not workspace-scoped) ----------------
case "$(uname -s)" in
  Darwin) CLAUDE_DESKTOP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json" ;;
  Linux)  CLAUDE_DESKTOP_CONFIG="$HOME/.config/Claude/claude_desktop_config.json" ;;
  *)      CLAUDE_DESKTOP_CONFIG="" ;;  # Windows: run this under WSL/Git Bash, or edit %APPDATA%\Claude\claude_desktop_config.json manually
esac

if [ -n "$CLAUDE_DESKTOP_CONFIG" ] && [ -d "$(dirname "$CLAUDE_DESKTOP_CONFIG")" ]; then
  "$PYTHON" "$HERE/_merge_config.py" "$CLAUDE_DESKTOP_CONFIG" mcpServers poetics-brand \
    "$PYTHON" "$SERVER_PATH"
else
  echo "Claude Desktop not detected, skipping (its config folder doesn't exist)."
fi

# -- Configure Windsurf (global config) -------------------------------------------
WINDSURF_CONFIG="$HOME/.codeium/windsurf/mcp_config.json"
if [ -d "$(dirname "$WINDSURF_CONFIG")" ]; then
  "$PYTHON" "$HERE/_merge_config.py" "$WINDSURF_CONFIG" mcpServers poetics-brand \
    "$PYTHON" "$SERVER_PATH"
else
  echo "Windsurf not detected, skipping (its config folder doesn't exist)."
fi

echo
echo "Done."
echo "VS Code, Cursor, and Claude Code need no separate step — they auto-configure"
echo "from .vscode/mcp.json, .cursor/mcp.json, and .mcp.json the moment you open this repo."
echo "Restart any editor you just configured above to pick up the new MCP server."
