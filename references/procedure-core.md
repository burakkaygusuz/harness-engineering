# Procedure: core

## Part A. Create the folders

1. Open a shell in the parent folder of the project.
2. Run these commands. Replace `<plugin-name>` and `<skill-name>` with your names. Run the last command again for each skill.

   ```bash
   mkdir -p <plugin-name>/{.claude-plugin,.agents/plugins}
   cd <plugin-name>
   mkdir -p skills/<skill-name>/{scripts,references,assets}
   ```

## Part B. Write the manifests and the packaging files

The three manifests use the same `name` and the same `description`.

1. Create the file `plugin.json` in the project root. Use this content:

   ```json
   {
     "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
     "name": "<plugin-name>",
     "version": "0.1.0",
     "description": "<one sentence that says what the plugin does>",
     "author": { "name": "<owner name>" },
     "license": "MIT",
     "keywords": ["<keyword>"]
   }
   ```

2. Create the file `.claude-plugin/plugin.json`. Use this content:

   ```json
   {
     "name": "<plugin-name>",
     "version": "0.1.0",
     "description": "<one sentence that says what the plugin does>",
     "author": { "name": "<owner name>" }
   }
   ```

3. Create the file `.claude-plugin/marketplace.json`. Use this content:

   ```json
   {
     "name": "<plugin-name>",
     "description": "<one sentence that says what the plugin does>",
     "owner": { "name": "<owner name>" },
     "plugins": [{ "name": "<plugin-name>", "source": "./" }]
   }
   ```

4. Create the file `.agents/plugins/marketplace.json` for Codex. Use the same `name` as in the manifests. Use this content:

   ```json
   {
     "name": "<plugin-name>",
     "plugins": [
       {
         "name": "<plugin-name>",
         "source": { "source": "local", "path": "./" },
         "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
         "category": "Productivity"
       }
     ]
   }
   ```

5. Create `LICENSE` with the full text of the license in `plugin.json`. Create `README.md`. In it, write what the plugin does and how to install it. Create `CHANGELOG.md` with one entry for version `0.1.0`.

## Part C. Write the skills

Do steps 1 to 8 for each skill.

1. Create the file `skills/<skill-name>/SKILL.md`. Start the file with this header:

   ```yaml
   ---
   name: <skill-name>
   description: <What the skill does, in the third person.> Use when <the situations that must start the skill>. Include the words that users write, for example "<phrase>".
   compatibility: Requires Python 3.11 or later. Uses the <agent-name> agent from this plugin if the client supports subagents. Otherwise works without a subagent.
   ---
   ```

   The `name` must be the same as the folder name. Omit `compatibility` if the skill needs no Python script and no agent.

2. Add the workflow to the body of the file. Use this text as a model:

   ```markdown
   ## Workflow

   1. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/<script-name>.py <input>` to get the data as JSON.
   2. Do the main task. Use `assets/<template>.md` for the output.
   3. If <a condition>, read `references/<topic>.md` first.
   4. Check the result. If the check fails, fix the problem and check again.
   5. If the agent `<agent-name>` or `<plugin-name>:<agent-name>` exists, give the task to it.
   6. If no subagent tool exists, do the work without a subagent.

   ## Available scripts

   - **`scripts/<script-name>.py`**: <What the script does.> Run it with `--help`.

   ## Gotchas

   - <A fact that the agent gets wrong without this warning.>
   ```

3. Create the script `skills/<skill-name>/scripts/<script-name>.py`. Start the file with this line:

   ```python
   #!/usr/bin/env python3
   ```

4. Add the `--help` option to the script. Use `argparse` from the Python standard library. Show the usage and the exit codes in the help text.
5. Make the script write JSON to standard output. Use a different exit code for each error type.
6. Do this step only for a skill that has an agent. Write the role text in `skills/<skill-name>/references/role.md`. The role text tells the agent what its job is and how to report. Start the role text with this step: read `AGENTS.md` at the project root, if the file exists. A Copilot subagent does not get the project instructions by default, and VS Code does not apply `include-custom-instructions` to plugin agents. The script `sync-agents.py` copies this file into the agent files.
7. Write the other long text in `skills/<skill-name>/references/<topic>.md`. Tell the agent in `SKILL.md` when to read each file.
8. Write each template in `skills/<skill-name>/assets/<template>.md`.

## Part D. Write AGENTS.md

`AGENTS.md` is a guide for the project. It lives in the project root, outside the plugin root. Do this Part after Part C. Do it before Part I.

1. Take the commands from Workflow step 1: build, test, lint, and type check. Take the rules that the agent cannot find in the code.
2. Look for `AGENTS.md` in the project root. If it exists, extend it. Do not replace it.
3. Write these sections. Leave out a section that has no content:
   - Build and test commands. Put each command in a code block.
   - Code style. Write only the rules that a linter does not enforce.
   - Prohibitions. Write what the agent must not do.
   - Plugin. Write one line that names the plugin skills and when to use them.
4. Write each instruction so that you can check it. Write "Run `npm test` before a commit". Do not write "Test your changes".
5. Keep the file short. Keep it under 200 lines and under 32 KiB. Move a long procedure to a skill.
6. Look for `CLAUDE.md` in the project root. If it exists, add the line `@AGENTS.md` to it. If it does not exist, do not create it.
7. Run each command in the file. Make sure that each command works. Fix the file for each command that fails.
