# Procedure: validate and release

## Part H. Validate and test

1. Validate each skill. Run the command for each skill:

   ```bash
   skills-ref validate skills/<skill-name>
   ```

2. Validate the plugin for Claude Code. Use version 2.1.289 or later. An older version checks only `marketplace.json`:

   ```bash
   claude plugin validate . --strict
   ```

3. Run the MCP check only when the plugin has `mcp.json`. The check needs Node.js 22.23.4, 24.22.1, or 26.12.1 or later. It needs uv only when the plugin has a server that you write. The first run needs network access. The check makes no model calls.

   ```bash
   python3 scripts/check-mcp.py
   ```

   Fix each failure, and run the check again, until it passes.

4. Run the plugin evals. Use Claude Code version 2.1.269 or later. The command grants the tools that the evals need. Bash runs in the operating system sandbox. Linux needs `bubblewrap` and `socat`. Windows needs WSL2. Git 2.31 or later is required. In a script or in CI, run the command once in a terminal first, or add `--trust-plugin` for a plugin that you trust.

   ```bash
   claude plugin eval . --scaffold --allow-tools Bash Write Edit
   ```

5. This command makes model calls. Model calls cost money.
6. Load the plugin in Claude Code:

   ```bash
   claude --plugin-dir .
   ```

7. Load the plugin in VS Code. Set `chat.plugins.enabled` to `true`. Add the project path to `chat.pluginLocations`. This setting is experimental. It also accepts `~/` and `./` paths:

   ```json
   "chat.pluginLocations": {
     "/path/to/<plugin-name>": true
   }
   ```

8. Make sure that both clients show the skills and the agents. An agent with `user-invocable: false` does not show in the agent picker. Look for it in the Agent Customizations editor, or ask the main agent to use it.
9. Test the install from the marketplace. Run the commands from the project root. Do not use `--plugin-dir`. Claude Code:

   ```bash
   claude plugin marketplace add .
   claude plugin install <plugin-name>@<plugin-name>
   ```

10. Start Claude Code. Make sure that the agents `<plugin-name>:<agent-name>` exist. Make sure that the skills exist.
11. Test the same install in Copilot CLI:

    ```bash
    copilot plugin marketplace add .
    copilot plugin install <plugin-name>@<plugin-name>
    copilot plugin list
    ```

12. Start Copilot CLI. Make sure that the agents `<agent-name>` and the skills exist.
13. Make the project a git repository. Run `git init` and commit, or push it to a remote. VS Code accepts only git repositories as marketplaces. In VS Code, add the repository to `chat.plugins.marketplaces`. For a local copy, use a `file:///` path. Install the plugin from the `@agentPlugins` view. Make sure that the agents and the skills appear.

## Part I. Release

1. Increase the `version` field in both manifests.
2. Write the changes in `CHANGELOG.md`.
3. Run `python3 scripts/sync-agents.py --check`. Run `python3 scripts/check-mcp.py` when the plugin has `mcp.json`. Then run the validation commands again.
4. Run `claude plugin details <plugin-name>`. Check the token cost of the descriptions.

## Final checklist

- [ ] The plugin name has only lowercase letters, numbers, and hyphens.
- [ ] Both manifests have the same version number.
- [ ] The folder name of each skill is the same as its `name` field.
- [ ] `skills-ref validate` passes for each skill.
- [ ] `claude plugin validate . --strict` passes.
- [ ] `python3 scripts/check-mcp.py` passes on both protocol eras, if the plugin has `mcp.json`.
- [ ] Each `SKILL.md` file has fewer than 500 lines and fewer than 5,000 tokens.
- [ ] The agent bodies are the same as the `role.md` files.
- [ ] `evals/results/` and `.workspace/` are in `.gitignore`.
- [ ] Both clients show the skills and the agents.
- [ ] The marketplace entry has the same `name` as the manifests and has no `version`.
- [ ] A marketplace install shows the skills and the agents in Claude Code, Copilot CLI, and VS Code.
