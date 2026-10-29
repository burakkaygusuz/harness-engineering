# Procedure: folders and manifests

## Part A. Create the folders

1. Open a shell in the parent folder of the project.
2. Run these commands. Replace `<plugin-name>` and `<skill-name>` with your names. Run the last two commands again for each skill.

   ```bash
   mkdir -p <plugin-name>/{.claude-plugin,.agents/plugins,agents,com.github.copilot/agents,scripts}
   mkdir -p <plugin-name>/evals/unrelated-request/graders
   cd <plugin-name>
   mkdir -p skills/<skill-name>/{scripts,references,assets,evals/files}
   mkdir -p evals/<skill-name>-task/graders
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
