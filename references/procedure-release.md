# Procedure: validate and release

## Part H. Validate and test

1. Run the validation commands in `SKILL.md`, section "Validation". Fix each failure. Then run the commands again. Do this until they pass.
2. If the user agrees, run the plugin evals with the command in `SKILL.md`, section "Validation". Bash runs in the operating system sandbox. Linux needs `bubblewrap` and `socat`. Windows needs WSL2. Before you run it in a script or in CI, run the command once in a terminal. For a plugin that you trust, you can add `--trust-plugin` instead.
3. Load the plugin in Claude Code:

   ```bash
   claude --plugin-dir .
   ```

4. Load the plugin in VS Code. Set `chat.plugins.enabled` to `true`. Add the project path to `chat.pluginLocations`. This setting is experimental. It also accepts `~/` and `./` paths:

   ```json
   "chat.pluginLocations": {
     "/path/to/<plugin-name>": true
   }
   ```

5. Make sure that both clients show the skills and the agents. The agent picker does not show an agent with `user-invocable: false`. Find it in the Agent Customizations editor, or ask the main agent to use it.
6. Test the install from the marketplace. Run the commands from the project root. Do not use `--plugin-dir`. Claude Code:

   ```bash
   claude plugin marketplace add .
   claude plugin install <plugin-name>@<plugin-name>
   ```

7. Start Claude Code. Make sure that the agents `<plugin-name>:<agent-name>` exist. Make sure that the skills exist.
8. Test the same install in Copilot CLI:

   ```bash
   copilot plugin marketplace add .
   copilot plugin install <plugin-name>@<plugin-name>
   copilot plugin list
   ```

9. Start Copilot CLI. Make sure that the agents `<agent-name>` and the skills exist.
10. Test the same install in Codex:

    ```bash
    codex plugin marketplace add .
    codex plugin add <plugin-name>@<plugin-name>
    codex plugin marketplace list
    ```

11. Start Codex. Make sure that the skills exist.
12. Make the project a git repository. Run `git init`. Then commit the files. You can also push the project to a remote. VS Code accepts only git repositories as marketplaces. In VS Code, add the repository to `chat.plugins.marketplaces`. For a local copy, use a `file:///` path. Install the plugin from the `@agentPlugins` view. Make sure that the agents and the skills appear.

## Part I. Release

1. Increase the `version` field in both manifests.
2. Write the changes in `CHANGELOG.md`.
3. Run `python3 scripts/sync-agents.py --check`. Then run the validation commands in `SKILL.md`, section "Validation", again.
4. Run `claude plugin details <plugin-name>`. Check the token cost of the descriptions.

## Final checklist

- [ ] The plugin obeys each rule in `references/rules.md`.
- [ ] `skills-ref validate` passes for each skill.
- [ ] `claude plugin validate . --strict` passes.
- [ ] `python3 scripts/check-mcp.py` passes on both protocol eras, if the plugin has `mcp.json`.
- [ ] `python3 scripts/sync-agents.py --check` shows no differences.
- [ ] `evals/results/` and `.workspace/` are in `.gitignore`.
- [ ] Both clients show the skills and the agents.
- [ ] A marketplace install shows the skills and the agents in Claude Code, Copilot CLI, and VS Code.
- [ ] A marketplace install shows the skills in Codex.
