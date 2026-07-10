#!/usr/bin/env python3
"""Safely merge the poetics-brand MCP server entry into an existing editor
config file, without touching any other servers already configured there.

Usage:
    python3 _merge_config.py <config_path> <top_level_key> <server_name> <command> <arg1> [arg2 ...]

Behavior:
  - Creates the config file (and parent dirs) if it doesn't exist.
  - If it exists, backs it up to <path>.bak before writing (only on first
    write in a session, and only if the content actually changes).
  - Only ever touches config[top_level_key][server_name] — every other key
    in the file, including other MCP servers, is left exactly as-is.
  - Idempotent: running it again with the same arguments is a no-op.
"""
import json
import pathlib
import sys


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    config_path = pathlib.Path(sys.argv[1]).expanduser()
    top_key = sys.argv[2]
    server_name = sys.argv[3]
    command = sys.argv[4]
    args = sys.argv[5:]

    entry = {"command": command, "args": args}

    if config_path.exists():
        try:
            data = json.loads(config_path.read_text())
        except json.JSONDecodeError:
            print(f"ERROR: {config_path} exists but isn't valid JSON — not touching it. "
                  f"Add this entry manually:\n{json.dumps({server_name: entry}, indent=2)}")
            sys.exit(1)
    else:
        data = {}
        config_path.parent.mkdir(parents=True, exist_ok=True)

    existing_top = data.get(top_key, {})
    if existing_top.get(server_name) == entry:
        print(f"already configured: {config_path}")
        return

    if config_path.exists():
        backup = config_path.with_suffix(config_path.suffix + ".bak")
        backup.write_text(config_path.read_text())

    data.setdefault(top_key, {})[server_name] = entry
    config_path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"configured: {config_path}")


if __name__ == "__main__":
    main()
