# Rules to follow

Write all text in the style of ASD-STE100 Issue 9. The author did not compare each word with the official dictionary. A full check needs the official dictionary from the ASD-STE100 website.

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
- Put the Claude Code agent files in `agents/`.
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
- Add the marketplace from a git source or a local folder. Relative paths do not resolve when a user adds only a URL of the `marketplace.json` file.

## Agents

- The Agent Plugins specification does not define agents as a portable component. Do not list agents in the root manifest.
- Claude Code adds the plugin name to the name of each component. The agent `<agent-name>` becomes `<plugin-name>:<agent-name>`.
- Write both names in the instructions of each `SKILL.md` file.

## MCP files

- Do not add an MCP file if you do not need one.
- Claude Code reads `.mcp.json`. The Agent Plugins format uses `mcp.json`. The two formats are different.
- Set `$schema` in `mcp.json` to the Agent Plugins MCP schema of the same version as `plugin.json`. Copilot CLI requires the two versions to be the same.
- Write the plugin root variable only in `args` and `env` values. Use `${PLUGIN_ROOT}` in `mcp.json` and `${CLAUDE_PLUGIN_ROOT}` in `.mcp.json`. The Agent Plugins format does not replace the variable in `command`. Claude Code does not replace it in `cwd`.

## Skill content

- Keep each `SKILL.md` file under 500 lines and under 5,000 tokens.
- Use only these fields in the frontmatter of `SKILL.md`: `name`, `description`, `license`, `allowed-tools`, `metadata`, and `compatibility`. `skills-ref validate` fails on other fields.
- Add a `## Gotchas` section to `SKILL.md` for facts that the agent gets wrong without a warning. Add each correction from the evals to this section.
- Cut each instruction that the agent follows correctly without it.
- If a skill makes the agent change files or data, add a step that checks the result. Make the agent fix the problem and check again until the check passes.
- Put long text in the `references/` folder.
- Tell the agent in `SKILL.md` when to read each reference file.
- Write relative paths from the skill folder in links to reference files. Use one folder level.
- Claude Code runs commands in the working directory of the session, not in the skill folder. In a command that runs a bundled script, write the path with `${CLAUDE_SKILL_DIR}`, for example `python3 ${CLAUDE_SKILL_DIR}/scripts/<script-name>.py`. Claude Code replaces the variable in the text of the skill. Use `${CLAUDE_PLUGIN_ROOT}` only for files that several skills share. The folder of the plugin changes with each version. Do not write it as a fixed path.
- Copilot CLI replaces `${PLUGIN_ROOT}` only in MCP and LSP server configurations and in the `mcp-servers` field of a plugin agent. VS Code replaces it in hook commands and MCP server configurations. Neither client defines a variable for skill text.

## Scripts

- Write each script in Python. Use the `.py` extension. Run it with `python3`.
- A shell script is allowed only for `fixture.sh`. Claude Code requires `fixture.sh` to be a Bash script.
- Use only the Python standard library. Do not add packages. Then the plugin has no install step, no `requirements.txt`, and no `pyproject.toml`.
- Write the data to standard output. Write messages and errors to standard error.
- Declare no dependencies. The plugin has nothing to install.
- Write the Python version in the `compatibility` field of each `SKILL.md` file that runs a Python script.

## Evals

- Put the skill evals in `skills/<name>/evals/`.
- Put the plugin evals in `evals/` at the project root.
- Keep the two eval systems in separate folders.
