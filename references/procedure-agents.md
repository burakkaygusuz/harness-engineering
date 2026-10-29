# Procedure: agent files

## Part E. Add the agent files

Do steps 1 to 4 for each agent. Give an agent only the tools that its role needs.

1. Create `agents/<agent-name>.md` for Claude Code. Use this header:

   ```markdown
   ---
   name: <agent-name>
   description: <What the agent does.> <When the main agent must use it.>
   tools: Read, Glob, Grep
   ---
   ```

   Add `Edit` and `Write` for an agent that changes files. Add `Bash` for an agent that runs commands. Add `WebFetch` for an agent that reads web pages.

2. Create `com.github.copilot/agents/<agent-name>.agent.md` for Copilot. Use this header:

   ```markdown
   ---
   name: <agent-name>
   description: <What the agent does.> <When the main agent must use it.>
   tools: ['read', 'search']
   ---
   ```

   Add `'edit'` for an agent that changes files. Add `'execute'` for an agent that runs commands. Add `'web'` for an agent that reads web pages. Add `user-invocable: false` to hide the agent from the picker. The main agent can still use it as a subagent.

3. Do not write a `model` field in the agent files, unless the agent needs a specific model. Then write the `model` field in both files. The two clients use different values for the same model. Do not copy the value from one file to the other.
   - Claude Code: `sonnet`, `opus`, `haiku`, `fable`, a full model ID, or `inherit`.
   - Copilot: a Copilot model ID. Do not use `model-policy`. VS Code does not apply it to plugin agents.
4. Write the script `scripts/sync-agents.py`. The script must copy each `references/role.md` file into the body of the matching agent files. The script must not change the frontmatter. The two formats use different frontmatter fields. Each client ignores the agent files of the other client.
5. Add the option `--check` to the script. The option shows the differences and does not change files.
