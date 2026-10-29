# Procedure: project instructions

## Part J. Write AGENTS.md

`AGENTS.md` is a guide for the project. It lives in the project root, outside the plugin root. Do this Part after Part C. Do it before Part H.

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
