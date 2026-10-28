# Procedure: skills

## Part C. Write the skills

Do steps 1 to 8 for each skill.

1. Create the file `skills/<skill-name>/SKILL.md`. Start the file with this header:

   ```yaml
   ---
   name: <skill-name>
   description: <What the skill does, in the third person.> Use when <the situations that must start the skill>. Include the words that users write, for example "<phrase>".
   compatibility: Requires Node.js 22.12 or later. Uses the <agent-name> agent from this plugin if the client supports subagents. Otherwise works without a subagent.
   ---
   ```

   The `name` must be the same as the folder name. Omit `compatibility` if the skill needs no Node.js script and no agent.

2. Add the workflow to the body of the file. Use this text as a model:

   ```markdown
   ## Workflow

   1. Run `node ${CLAUDE_SKILL_DIR}/scripts/<script-name>.mjs <input>` to get the data as JSON.
   2. Do the main task. Use `assets/<template>.md` for the output.
   3. If <a condition>, read `references/<topic>.md` first.
   4. Check the result. If the check fails, fix the problem and check again.
   5. If the agent `<agent-name>` or `<plugin-name>:<agent-name>` exists, give the task to it.
   6. If no subagent tool exists, do the work without a subagent.

   ## Available scripts

   - **`scripts/<script-name>.mjs`**: <What the script does.> Run it with `--help`.

   ## Gotchas

   - <A fact that the agent gets wrong without this warning.>
   ```

3. Create the script `skills/<skill-name>/scripts/<script-name>.mjs`. Start the file with this line:

   ```js
   #!/usr/bin/env node
   ```

4. Add the `--help` option to the script. Use `parseArgs` from `node:util`. Show the usage and the exit codes in the help text.
5. Make the script write JSON to standard output. Write messages and errors to standard error. Use a different exit code for each error type.
6. Write the role text in `skills/<skill-name>/references/role.md`. The role text tells the agent what its job is and how to report. Start the role text with this step: read `AGENTS.md` at the project root, if the file exists. A Copilot subagent does not get the project instructions by default, and VS Code does not apply `include-custom-instructions` to plugin agents. The script `sync-agents.sh` copies this file into the agent files.
7. Write the other long text in `skills/<skill-name>/references/<topic>.md`. Tell the agent in `SKILL.md` when to read each file.
8. Write each template in `skills/<skill-name>/assets/<template>.md`.
