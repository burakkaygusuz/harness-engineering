---
name: harness-engineering
description: Use this skill when the user wants to set up, extend, or check an agent harness for a code project. Also use it when the user wants coding agents to follow project rules. Also use it to scaffold, validate, or release the Claude Code and GitHub Copilot plugin that carries the harness. It packages skills, MCP servers, reviewer agents, and evals as one Agent Plugins 1.0 plugin.
compatibility: Requires Python 3.11 or later. Uses the claude CLI (version 2.1.289 or later) and skills-ref (a Python package) for validation. The plugin evals also need Git 2.31 or later. An MCP server needs uv, and the MCP check needs Node.js 22.23.4, 24.22.1, or 26.12.1 or later.
---

# Harness engineering

Use this skill to build an agent harness for one code project. A harness is everything in an agent except the model. The harness has guides, which steer the agent before it acts, and sensors, which observe the agent after it acts. The plugin carries the harness for Claude Code and GitHub Copilot. Read `references/harness.md` for the model and the mapping from each harness part to a file.

The examples in the reference files use placeholders such as `<plugin-name>` and `<skill-name>`. Replace each placeholder with the name that the user gives.

## Workflow

1. Analyze the project. Find the test, lint, and type-check commands. A project without these commands has no computational sensor to build on. Tell the user what is missing.
2. Ask the user for the plugin name, the skill names, and the purpose of each skill. Ask which skills need an agent file.
3. Read `references/rules.md`. Check the plugin name against the rules. Do not use a reserved name.
4. Read `references/harness.md` to see the target folder tree.
5. Do the procedure in order. Read each file only when you reach its Part:
   - Parts A and B, folders and manifests (packaging): `references/procedure-scaffold.md`
   - Part C, skills (guides): `references/procedure-skills.md`
   - Part D, MCP servers (guide tools, optional): `references/procedure-mcp.md`
   - Part E, agent files (inferential sensors): `references/procedure-agents.md`
   - Parts F and G, skill evals and plugin evals: `references/procedure-evals.md`
   - Parts H and I, validation, release, and the final checklist: `references/procedure-release.md`
6. After each Part, check the result before you start the next Part.
7. Write all new text in the style of ASD-STE100 Simplified Technical English. Use short sentences, the imperative form, and the active voice.
8. Write scripts in Python. Use the `.py` extension. Shell scripts are allowed only where `references/rules.md` says so.

## Validation

Run these commands from the project root:

```bash
skills-ref validate skills/<skill-name>
claude plugin validate . --strict
```

Run `claude plugin eval . --scaffold --allow-tools Bash Write Edit` only when the user agrees. This command makes model calls and costs money.

## Gotchas

- Use the same `name` in `plugin.json`, `.claude-plugin/plugin.json`, and the marketplace entry. An install by name fails if the names differ.
- Keep the same `version` in both manifests. Do not set `version` in the marketplace entry.
- Claude Code reads `agents/`. Copilot reads `com.github.copilot/agents/`. Each client ignores the other folder.
- Claude Code runs commands in the working directory of the session, not in the skill folder. Write the path to a bundled script with `${CLAUDE_SKILL_DIR}`. Use `${CLAUDE_PLUGIN_ROOT}` only for files that several skills share. Copilot defines no variable for skill text.
- Grant `Bash` to the plugin evals only with `--allow-tools`. Do not list it in `prompt.md`.
- Add no packages to the scripts. Use only the Python standard library. The one exception is an MCP server in `servers/`. It declares the `mcp` SDK in its script header.
- Do not write a `print` call in an MCP server. Standard output carries only MCP messages.
- Apply the gate in `references/procedure-mcp.md` before you add an MCP server. The default outcome is no server.

## Sources

Read `references/sources.md` to find the official documents and the harness engineering sources that this skill follows.
