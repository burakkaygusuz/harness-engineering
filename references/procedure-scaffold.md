# Procedure: folders and manifests

## Part A. Create the folders

1. Open a shell in the parent folder of the project.
2. Run these commands. Replace `<plugin-name>` and `<skill-name>` with your names. Run the last two commands again for each skill.

   ```bash
   mkdir -p <plugin-name>/{.claude-plugin,agents,com.github.copilot/agents,scripts}
   mkdir -p <plugin-name>/evals/unrelated-request/graders
   cd <plugin-name>
   mkdir -p skills/<skill-name>/{scripts,references,assets,evals/files}
   mkdir -p evals/<skill-name>-task/graders
   ```

3. Only for a Python MCP server, run `mkdir -p servers` in the project root. Skip this step for an existing server.

## Part B. Write the manifests

All three files use the same `name` and the same `description`.

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
