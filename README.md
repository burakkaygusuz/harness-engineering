# agent-plugin-setup

An agent skill that guides an agent through the build of an agent harness for a code project. The harness follows the harness engineering model: guides steer the agent before it acts, and sensors check the agent after it acts. The skill packages the harness as one Agent Plugins 1.0 plugin with agent skills, agent files, skill evals, and plugin evals. It works with Claude Code and GitHub Copilot.

## Contents

- `SKILL.md`: the skill. It has the workflow and the validation commands.
- `references/`: focused files that the agent reads only when needed:
  - `rules.md` and `harness.md`: the rules, and the harness model with the target folder tree.
  - `procedure-*.md`: the steps for each Part of the setup.
  - `sources.md`: the official documents.

## Requirements

- Python 3.11 or later.
- The `claude` CLI, version 2.1.289 or later, for `claude plugin validate`. Use version 2.1.269 or later for `claude plugin eval`.
- Git 2.31 or later, for `claude plugin eval`. The eval also needs the operating system sandbox: `bubblewrap` and `socat` on Linux, WSL2 on Windows.
- `skills-ref`, to validate the skills. It is a Python package. Install it from the `skills-ref` folder of the `agentskills/agentskills` repository.

## Install

Copy the `agent-plugin-setup` folder into the skills folder of your client. For Claude Code, use `~/.claude/skills/`.

## Use

Ask the agent to set up an agent plugin project. The agent loads the skill and follows the procedure in `references/`.

## License

MIT. See `LICENSE`.
