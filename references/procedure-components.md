# Procedure: components

Do a Part in this file only when the plugin needs the component.

## Part E. Add MCP servers

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

   Name each command that the server needs, such as `uv` or `npx`. Write each command in the `compatibility` field of each skill that uses the server. Also write each command in the plugin `README.md`.

6. Tell the user, in the plugin `README.md`, to run `uv sync --script servers/<server-name>.py` once before first use. The first start can download Python and the SDK, and it can pass the startup timeout of Claude Code (`MCP_TIMEOUT`). After a failed start, Claude Code skips a plugin server for 15 minutes.

7. Copy the file `scripts/check-mcp.py` of this skill into the `scripts/` folder of the plugin. Run `python3 scripts/check-mcp.py` from the plugin root. Fix the server or the entry. Then run the check again. Do this until it passes. If it still fails, tell the user why, and do not ship the server.

   The script is a computational sensor. It checks the lock files, `mcp.json`, and the drift between `mcp.json` and `.mcp.json`. Then it runs the MCP Inspector on each entry, once for each protocol era. The first run needs network access, because it downloads the Inspector. The check makes no model calls.

8. In `AGENTS.md`, or in the skill that uses the tools, write when the agent calls each tool.

## Part F. Add the agent files

Do steps 1 to 3 for each agent. Do steps 4 and 5 one time. Give an agent only the tools that its role needs.

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
4. Write the script `scripts/sync-agents.py`. The script must copy each `references/role.md` file into the body of the agent files that match. The script must not change the frontmatter. The two formats use different frontmatter fields. Each client ignores the agent files of the other client.
5. Add the option `--check` to the script. The option shows the differences and does not change files.

## Part G. Add the skill evals

Do steps 1 to 5 for each skill.

1. Write the file `skills/<skill-name>/evals/evals.json`. Start with two or three test cases. Use this model:

   ```json
   {
     "skill_name": "<skill-name>",
     "evals": [
       {
         "id": 1,
         "prompt": "<A realistic request, as a user writes it.>",
         "expected_output": "<A short description of a good answer.>",
         "files": ["evals/files/<input-file>"],
         "assertions": [
           "<A statement that is true or false for the output>",
           "<Another statement that is true or false for the output>"
         ]
       },
       {
         "id": 2,
         "prompt": "<A second request. Make it different from the first request.>",
         "expected_output": "<A short description of a good answer.>",
         "files": ["evals/files/<other-input-file>"]
       }
     ]
   }
   ```

2. Add more assertions after you read the first outputs. Add each failure that you find to the `## Gotchas` section of the skill.
3. Write the file `skills/<skill-name>/evals/train_queries.json`. Include queries that must start the skill and queries that must not start it.
4. Add near-miss queries that must not start the skill. A near-miss query uses words that are close to the skill but asks for a different task. Use this model:

   ```json
   [
     { "query": "<A request that the skill must handle>", "should_trigger": true },
     {
       "query": "<A request that is close to the skill but is a different task>",
       "should_trigger": false
     },
     {
       "query": "<A request that has no link to the skill>",
       "should_trigger": false
     }
   ]
   ```

5. Write the file `skills/<skill-name>/evals/validation_queries.json` with different queries. Do not use the same queries in both files.

## Part H. Add the plugin evals

Do steps 1 to 5 for each skill. Do steps 6 to 8 one time.

1. Create the file `evals/<skill-name>-task/prompt.md`:

   ```markdown
   ---
   max_turns: 15
   allowed_tools: [Read, Glob, Grep, Skill, Agent]
   ---

   <A request that must start the skill. Write it as a user types it. Do not name the skill. Name the input files that the fixture creates.>
   ```

2. Create the file `evals/<skill-name>-task/case.yaml`:

   ```yaml
   schema_version: '1.1'
   name: <skill-name>-task
   tags: [smoke]
   context:
     scaffold_script: fixture.sh
   ```

3. Write the script `evals/<skill-name>-task/fixture.sh`. Claude Code requires a Bash script. Make the script write the input files into the workspace.
4. Create the grader `evals/<skill-name>-task/graders/criteria.md`:

   ```markdown
   ---
   type: llm
   ---

   PASS if <the condition for a correct answer>.
   FAIL if <the condition for a wrong answer>.
   ```

5. Create the grader `evals/<skill-name>-task/graders/skill-fired.md`. This grader shows if the skill started. In a run with two arms, the score does not include it. Use `criteria.md` for the score:

   ```markdown
   ---
   type: tool_used
   tool: Skill
   input_match: '"skill"\s*:\s*"(?:[\w-]+:)?<skill-name>"'
   ---
   ```

6. Create the file `evals/unrelated-request/prompt.md`. Write one request that has no link to the skills, for example `Write a haiku about autumn.`
7. Create the grader `evals/unrelated-request/graders/no-skill.md`. This grader checks that no skill started:

   ```markdown
   ---
   type: tool_used
   tool: Skill
   arm: both
   min: 0
   max: 0
   ---
   ```

8. Create the file `.gitignore` with this content:

   ```txt
   evals/results/
   .workspace/
   ```
