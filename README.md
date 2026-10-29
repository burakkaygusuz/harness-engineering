# harness-engineering

An agent skill that guides an agent through the build of an agent harness for a code project. The harness follows the harness engineering model: guides steer the agent before it acts, and sensors check the agent after it acts. The skill packages the harness as one Agent Plugins 1.0 plugin with agent skills, agent files, skill evals, and plugin evals. It works with Claude Code and GitHub Copilot.

## Contents

- `SKILL.md`: the skill. It has the workflow and the validation commands.
- `references/`: focused files that the agent reads only when needed:
  - `rules.md` and `harness.md`: the rules, and the harness model with the target folder tree.
  - `procedure-*.md`: the steps for each Part of the setup.

## Requirements

- Python 3.11 or later.
- The `claude` CLI, version 2.1.289 or later, for `claude plugin validate`. Use version 2.1.269 or later for `claude plugin eval`.
- Git 2.31 or later, for `claude plugin eval`. The eval also needs the operating system sandbox: `bubblewrap` and `socat` on Linux, WSL2 on Windows.
- `uv`, for an MCP server that you write.
- Node.js 22.23.4, 24.22.1, or 26.12.1 or later, for the MCP check. The check runs the MCP Inspector with `npx`.
- `skills-ref`, to validate the skills. It is a Python package. Install it from the `skills-ref` folder of the `agentskills/agentskills` repository.

## Install

Copy the `harness-engineering` folder into the skills folder of your client. For Claude Code, use `~/.claude/skills/`.

## Use

Ask the agent to set up an agent harness for your project. The agent loads the skill and follows the procedure in `references/`.

## Style

The skill text follows ASD-STE100 Simplified Technical English, Issue 9. The author did not compare each word with the official dictionary. A full check needs the official dictionary from the ASD-STE100 website.

## Sources

The skill files do not cite their sources. The agent reads them at run time, and a citation does not change what the agent does. Each token that the agent does not need costs context. See [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices) and [Claude skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

The git history keeps the sources. Each commit that adds or changes a fact lists its sources in the commit body. To find the source of a line, run `git blame` on the line and read the commit body.

These rules apply to the sources:

- A design rule in the skill needs two or more independent Tier 1 or Tier 2 sources. A commit that adds a rule with only one source says so.
- The model terms come from Böckeler: harness, guide, sensor, computational, inferential, and steering loop. A definition needs one source.
- File formats and client behavior come only from official documents.

The tiers:

- Tier 1: first-party engineering posts and formats, from OpenAI, Anthropic, LangChain, and Cursor, and the AGENTS.md format.
- Tier 2: recognized practitioners: Birgitta Böckeler and Mitchell Hashimoto.
- Tier 3: a reading list. No claim in the skill rests on it: [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) and [awesome-harness-engineering](https://github.com/walkinglabs/awesome-harness-engineering).

## License

MIT. See `LICENSE`.
