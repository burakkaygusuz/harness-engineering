# Rules to follow

Write all new text in the style of ASD-STE100 Simplified Technical English, Issue 9. Use short sentences, the imperative form, and the active voice.

## Names

- Use only lowercase letters, numbers, and hyphens in the plugin name.
- Do not start the plugin name with `claude-`, `anthropic-`, `anthropics-`, or `cc-plugin-`.
- Do not use the names `claude`, `anthropic`, `anthropics`, `claude-code`, or `claude-mods`.
- Do not use `claude`, `anthropic`, or `anthropics` as a whole word anywhere else in the name. `claude plugin validate` shows a warning.
- Do not put `official` next to `claude` or `anthropic` in the name.
- `claude plugin validate` shows an error for these names.
- Do not start or end the plugin name with a hyphen. Do not use two hyphens in a row.
- Use 64 characters or fewer in the plugin name.
- Make the folder name of each skill the same as the `name` field in its `SKILL.md` file.

## Folders

- Put each skill folder directly in `skills/`. The clients do not search deeper folders.
- Put the agent files for Claude Code in `agents/`.
- Put the Copilot agent files in `com.github.copilot/agents/`.
- Do not put other files in `skills/`.

## Manifests

- Use the root `plugin.json` for the Agent Plugins format. The schema is closed. Use only the fields that the schema lists: `$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and `extensions`. Put client data only in `extensions`, under a reverse-domain namespace.
- Use `.claude-plugin/plugin.json` for Claude Code. Claude Code reads only this file and ignores the root `plugin.json`.
- Set `$schema` in the root `plugin.json` to the exact URL `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`. Copilot CLI reads the Agent Plugins format only when the value is exact. Without the value, Copilot CLI reads the legacy format. Copilot CLI rejects an Agent Plugins version that it does not support.
- Copilot CLI gives the root `plugin.json` priority over `.claude-plugin/plugin.json`. VS Code finds the format from the root manifest and the format-specific paths.
- Keep the same version number in both manifests.
- Change the version number for each release. Claude Code keeps each user on the same version until the field changes.

## Marketplace

- Put the catalog in `.claude-plugin/marketplace.json`. Claude Code reads this path. Copilot CLI and VS Code also read it.
- Use one plugin entry. Set `source` to `"./"`, the repository root. Claude Code resolves `source` from the folder that contains `.claude-plugin/`.
- Give the entry the same `name` as the plugin manifests. An install by the manifest name fails when the names are different.
- Do not set `version` in the entry. Set it only in the two manifests. Then the version has one owner.
- Do not set component fields such as `agents` in the entry. The manifests and the fixed folders define the components.
- Do not use a reserved marketplace name. Claude Code reserves names such as `claude-plugins-official` and `anthropic-plugins`. Claude Code also blocks names that look like them.
- Put the Codex catalog in `.agents/plugins/marketplace.json`. Give each entry `source`, `policy.installation`, `policy.authentication`, and `category`. Write `source` as an object with `"source": "local"` and a `path` that starts with `./`. Use `AVAILABLE` for `policy.installation` and `ON_INSTALL` for `policy.authentication`. Codex resolves `path` from the marketplace root, not from `.agents/plugins/`.
- Add the marketplace from a git source or a local folder. Relative paths do not resolve when a user adds only a URL of the `marketplace.json` file.

## Agents

- The Agent Plugins specification does not define agents as a portable component. Do not list agents in the root manifest.
- Claude Code adds the plugin name to the name of each component. The agent `<agent-name>` becomes `<plugin-name>:<agent-name>`.
- Write both names in the instructions of each `SKILL.md` file.
- Claude Code ignores the fields `permissionMode`, `hooks`, `mcpServers`, and `initialPrompt` in a plugin agent file. Add hooks and MCP servers to the plugin instead.
- Cursor reads Markdown agents from `.cursor/agents/`. Codex reads only TOML agents from `.codex/agents/`. Neither client has a `tools` field. Do not generate agent files for Cursor and Codex. Codex ignores `sandbox_mode` in an agent file.

## MCP servers

- Do not add an MCP server by default. Give the agent the project's commands, scripts, and CLIs first.
- Make an action that must run on every event a hook, not a tool.
- Add an MCP server only for external data or actions, such as a database.
- Do not make a tool that only wraps software functionality or an API endpoint that already exists.
- Do not add an MCP server for an end-to-end behavior check of the product.
- Each tool adds text to the context. More tools do not always lead to better outcomes. Keep the number of tools low.
- Reject a server that answers only the earlier handshake. MCP 2026-07-28 requires `server/discover`.
- Serve both protocol eras. A server that serves only 2026-07-28 fails for a client that uses only the earlier handshake.
- Claude Code's v1 runtime and `MCP_PROTOCOL_NEGOTIATION=legacy` use only the earlier handshake.
- Copilot CLI before v1.0.81 predates 2026-07-28 support.
- Claude Code reads `.mcp.json`. The Agent Plugins format uses `mcp.json`. The two formats are different.
- Set `$schema` in `mcp.json` to the Agent Plugins MCP schema of the same version as `plugin.json`. Copilot CLI requires the two versions to be the same.
- Set `"type": "stdio"` for each server.
- Write `command` as a bare program name, such as `uv` or `npx`. The Agent Plugins format does not replace variables in `command`.
- Write the plugin root variable only in `args` and `env` values. Use `${PLUGIN_ROOT}` in `mcp.json` and `${CLAUDE_PLUGIN_ROOT}` in `.mcp.json`. Claude Code does not replace it in `cwd`.
- The Agent Plugins specification requires clients to replace `${PLUGIN_ROOT}` in `args`, `env`, and `cwd`. Cursor documents that it does not. The source code of Codex does it in `mcp.json`, but no Codex release is confirmed to include it. Do not promise that a server that you write works in Cursor and Codex.
- The server starts in the plugin root, not in the project. Take the project folder as the `project_dir` parameter of each tool.
- Do not use Roots, Sampling, or Logging in a server. They are deprecated. Tool parameters replace Roots.
- Do not use `ctx.elicit()`. It fails on a 2026-07-28 connection. When a tool must ask the user, use `Resolve` or `Elicit` from `mcp.server.mcpserver`.
- Write no protocol code in a server. The SDK answers `server/discover` on stdio and serves both protocol eras.

## Skill content

- Keep each `SKILL.md` file under 500 lines and under 5,000 tokens.
- Use only these fields in the frontmatter of `SKILL.md`: `name`, `description`, `license`, `allowed-tools`, `metadata`, and `compatibility`. `skills-ref validate` fails on other fields.
- Add a `## Gotchas` section to `SKILL.md` for facts that the agent gets wrong without a warning.
- Cut each instruction that the agent follows correctly without it.
- If a skill makes the agent change files or data, add a step that checks the result. Make the agent fix the problem. Then make the agent check again. Do this until the check passes.
- Put long text in the `references/` folder.
- Tell the agent in `SKILL.md` when to read each reference file.
- Write relative paths from the skill folder in links to reference files. Use one folder level.
- Claude Code runs commands in the working directory of the session, not in the skill folder. In a command that runs a bundled script, write the path with `${CLAUDE_SKILL_DIR}`, for example `python3 ${CLAUDE_SKILL_DIR}/scripts/<script-name>.py`. Claude Code replaces the variable in the text of the skill. Use `${CLAUDE_PLUGIN_ROOT}` only for files that several skills share. The folder of the plugin changes with each version. Do not write it as a fixed path.
- Copilot CLI replaces `${PLUGIN_ROOT}` only in MCP and LSP server configurations and in the `mcp-servers` field of a plugin agent. VS Code replaces it in hook commands and MCP server configurations. Neither client defines a variable for skill text.

## Scripts

- Write each script in Python. Use the `.py` extension. Run it with `python3`.
- Use a shell script only for `fixture.sh`. Claude Code requires `fixture.sh` to be a Bash script.
- Use only the Python standard library in scripts. Do not add packages. Then the scripts have no install step, no `requirements.txt`, and no `pyproject.toml`.
- Write the data to standard output. Write messages and errors to standard error.
- An MCP server that you write is the one exception. It uses the official Python SDK for MCP, version 2.x (`mcp>=2,<3`). Declare the SDK in the script header (PEP 723). Lock it with `uv lock --script`. It writes only MCP messages to standard output and writes logs to standard error.
- Write the Python version in the `compatibility` field of each `SKILL.md` file that runs a Python script.

## Evals

- Put the skill evals in `skills/<name>/evals/`.
- Put the plugin evals in `evals/` at the project root.
- Keep the two eval systems in separate folders.
- Cursor and Codex have no documented command to validate or evaluate a plugin. Run the plugin evals in Claude Code only.
