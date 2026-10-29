#!/usr/bin/env python3
"""Check the MCP files of a plugin on both protocol eras.

Run it from the plugin root. It checks mcp.json, .mcp.json, the lock file of
each server in servers/, and runs the MCP Inspector on each entry.

Exit codes: 0 = all checks pass, 1 = a check fails, 2 = bad usage.
Output: JSON on standard output. Messages on standard error.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

# Before you raise the version, read https://github.com/modelcontextprotocol/inspector/security/advisories
INSPECTOR = "@modelcontextprotocol/inspector@2.13.0"
ENTRY_KEYS = {"type", "command", "args", "env", "cwd"}


def schema_version(doc):
    # .../schemas/<version>/<name>.schema.json
    parts = doc.get("$schema", "").split("/")
    return parts[-2] if len(parts) >= 2 else ""


def swap(value, old, new):
    return json.loads(json.dumps(value).replace(old, new))


def check_files(root, errors):
    for server in sorted(root.glob("servers/*.py")):
        r = subprocess.run(["uv", "lock", "--script", str(server), "--check"],
                           capture_output=True, text=True)
        if r.returncode:
            errors.append(f"{server.name}: lock file is missing or out of date")
    mcp = json.loads((root / "mcp.json").read_text())
    if set(mcp) != {"$schema", "mcpServers"}:
        errors.append("mcp.json: top-level keys must be $schema and mcpServers")
    plugin = json.loads((root / "plugin.json").read_text())
    if schema_version(mcp) != schema_version(plugin):
        errors.append("mcp.json: $schema version differs from plugin.json")
    for name, e in mcp.get("mcpServers", {}).items():
        if e.get("type") != "stdio" or not e.get("command"):
            errors.append(f"{name}: needs type stdio and a command")
        if set(e) - ENTRY_KEYS:
            errors.append(f"{name}: unknown keys {sorted(set(e) - ENTRY_KEYS)}")
        if "${" in e.get("command", "") or "${" in e.get("cwd", ""):
            errors.append(f"{name}: command and cwd must not hold a variable")
        if {"PLUGIN_ROOT", "PLUGIN_DATA"} & set(e.get("env", {})):
            errors.append(f"{name}: env must not set PLUGIN_ROOT or PLUGIN_DATA")
    claude = json.loads((root / ".mcp.json").read_text())
    want = swap(mcp.get("mcpServers", {}), "${PLUGIN_ROOT}", "${CLAUDE_PLUGIN_ROOT}")
    if claude.get("mcpServers") != want:
        errors.append(".mcp.json: drift from mcp.json")
    return mcp.get("mcpServers", {})


def run_inspector(root, name, entry, era, data_dir, errors):
    def sub(v):
        return v.replace("${PLUGIN_ROOT}", str(root)).replace("${PLUGIN_DATA}", data_dir)

    target = ["--cli", entry["command"], *map(sub, entry.get("args", []))]
    for k, v in entry.get("env", {}).items():
        target[:0] = ["-e", f"{k}={sub(v)}"]
    if "cwd" in entry:
        target[:0] = ["--cwd", entry["cwd"]]
    cmd = ["npx", "-y", INSPECTOR]
    # target options go before the "--" that separates the Inspector options
    cmd += target + ["--", "--protocol-era", era, "--method", "tools/list", "--strict"]
    r = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
    if r.returncode:
        errors.append(f"{name}: {era} run failed: {(r.stderr or r.stdout).strip()[-300:]}")


def self_test():
    """Check the file checks on a bad fixture. Needs no network and no uv."""
    entry = {"type": "stdio", "command": "uv", "args": ["${PLUGIN_ROOT}/a"]}
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "plugin.json").write_text('{"$schema": "x/schemas/1.0.0/p.json"}')
        mcp = {"$schema": "x/schemas/1.0.0/m.json", "mcpServers": {"s": dict(entry, cwd="${bad}")}}
        (root / "mcp.json").write_text(json.dumps(mcp))
        claude = {"mcpServers": {"s": dict(entry, args=["${CLAUDE_PLUGIN_ROOT}/a"], cwd="${bad}")}}
        (root / ".mcp.json").write_text(json.dumps(claude))
        errors = []
        check_files(root, errors)
        assert errors == ["s: command and cwd must not hold a variable"], errors
        (root / ".mcp.json").write_text('{"mcpServers": {}}')
        errors = []
        check_files(root, errors)
        assert ".mcp.json: drift from mcp.json" in errors, errors
    print("self-test passed")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--self-test", action="store_true", help="run the built-in check and exit")
    if p.parse_args().self_test:
        self_test()
        return 0
    root = Path.cwd()
    errors = []
    try:
        servers = check_files(root, errors)
    except (OSError, ValueError) as e:
        print(f"cannot read the MCP files: {e}", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory() as data_dir:
        for name, entry in servers.items():
            for era in ("modern", "legacy"):
                run_inspector(root, name, entry, era, data_dir, errors)
    for e in errors:
        print(e, file=sys.stderr)
    print(json.dumps({"ok": not errors, "errors": errors}))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
