# Procedure: MCP servers

## Part D. Add MCP servers

1. Apply the rules in `references/rules.md`, section "MCP servers". If they do not allow a server, tell the user which script or hook does the job. Then skip this Part. The default outcome is no server.

2. Find a maintained server that already exists and does the job. If one exists, use it:
   1. Pin its exact version. Do not use a range or `latest`.
   2. Write its entry in step 5. Skip steps 3, 4, and 6.

3. Otherwise, run `mkdir -p servers`. Write `servers/<server-name>.py` from this skeleton:

   ```python
   #!/usr/bin/env -S uv run --script
   # /// script
   # requires-python = ">=3.11"
   # dependencies = ["mcp>=2,<3"]
   # ///
   """<server-name>: <one-line purpose>."""
   from pathlib import Path

   from mcp.server import MCPServer

   mcp = MCPServer("<server-name>")

   @mcp.tool()
   def <tool_name>(project_dir: str, <args>) -> dict:
       """<What the tool does and when the agent calls it.>

       project_dir is the project root. It is not a sandbox.
       """
       root = Path(project_dir).resolve(strict=True)
       ...

   if __name__ == "__main__":
       mcp.run(transport="stdio")
   ```

   Follow the server rules in `references/rules.md`, section "MCP servers".

4. Run `uv lock --script servers/<server-name>.py`. This writes `servers/<server-name>.py.lock`. Commit the lock file with the server.

5. Write the entry in `mcp.json` and the same entry in `.mcp.json`. For a server that you write, use `uv`. For a server that already exists, use `"command": "npx"` and `"args": ["-y", "<package>@<exact-version>"]`.

   In `mcp.json`, use the Agent Plugins variable `${PLUGIN_ROOT}`:

   ```json
   {
     "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
     "mcpServers": {
       "<server-name>": {
         "type": "stdio",
         "command": "uv",
         "args": ["run", "--frozen", "--script", "${PLUGIN_ROOT}/servers/<server-name>.py"]
       }
     }
   }
   ```

   In `.mcp.json`, use the Claude Code variable `${CLAUDE_PLUGIN_ROOT}`:

   ```json
   {
     "mcpServers": {
       "<server-name>": {
         "type": "stdio",
         "command": "uv",
         "args": ["run", "--frozen", "--script", "${CLAUDE_PLUGIN_ROOT}/servers/<server-name>.py"]
       }
     }
   }
   ```

   Use `--frozen`. It runs the server and does not change the lock file. The plugin root changes when the plugin updates, so do not write files there.

6. Tell the user, in the plugin `README.md`, to run `uv sync --script servers/<server-name>.py` once before first use. The first start can download Python and the SDK, and it can pass the startup timeout of Claude Code (`MCP_TIMEOUT`). After a failed start, Claude Code skips a plugin server for 15 minutes.

   Name each command that the server needs, such as `uv` or `npx`. Write each command in the `compatibility` field of each skill that uses the server. Also write each command in the plugin `README.md`.

7. Write `scripts/check-mcp.py` as specified below. Run `python3 scripts/check-mcp.py`. Fix the server or the entry. Then run the check again. Do this until it passes. If it still fails, tell the user why, and do not ship the server.

   The script `scripts/check-mcp.py` is a computational sensor for the MCP files. It uses only the Python standard library. It does these steps in order:
   1. Hold the Inspector package as one constant: `@modelcontextprotocol/inspector@2.13.0`. Before you raise the version, check the [Inspector security advisories](https://github.com/modelcontextprotocol/inspector/security/advisories).
   2. For each `servers/<name>.py` file, run `uv lock --script servers/<name>.py --check`. The command fails if the lock file does not exist or is out of date.
   3. Check `mcp.json`:
      - Its top-level keys are exactly `$schema` and `mcpServers`.
      - The Agent Plugins version in its `$schema` value equals the version in the `$schema` value of `plugin.json`.
      - Each entry has `"type": "stdio"` and a `command`. Its keys are a subset of `type`, `command`, `args`, `env`, and `cwd`.
      - `command` and `cwd` have no `${`.
      - `env` does not set `PLUGIN_ROOT` or `PLUGIN_DATA`.
   4. Check that the `mcpServers` of `.mcp.json` equal the `mcpServers` of `mcp.json`, after you replace `${PLUGIN_ROOT}` with `${CLAUDE_PLUGIN_ROOT}`. Claude Code reads only `.mcp.json`. Report each difference as drift.
   5. Replace `${PLUGIN_ROOT}` with the plugin root in `args` and `env`. Replace `${PLUGIN_DATA}` with a temporary folder only if an entry uses it.
   6. For each entry, run these two commands from the plugin root. Use the mapped `command` and `args` as the target:

      ```bash
      npx -y @modelcontextprotocol/inspector@<inspector-version> --cli <command> <args...> -- --protocol-era modern --method tools/list --strict
      npx -y @modelcontextprotocol/inspector@<inspector-version> --cli <command> <args...> -- --protocol-era legacy --method tools/list --strict
      ```

      `<inspector-version>` is the version in item 1. Before `--`, add one `-e KEY=VALUE` for each mapped `env` entry, and one `--cwd <path>` for the `cwd` entry. These are target options.

      The `modern` run pins 2026-07-28 with no fallback. The `legacy` run uses the earlier `initialize` handshake. The `--` separates the target from the Inspector options. `--strict` fails the run on a tool-schema portability problem.
   7. Any non-zero Inspector exit fails the check.
   8. Exit with code 1 if any check fails. Otherwise exit with code 0.

   The first run needs network access, because it downloads the Inspector. The check makes no model calls.

8. In `AGENTS.md`, or in the skill that uses the tools, write when the agent calls each tool.
