# Agent harness

This file explains the harness model. It maps each harness part to a file in the plugin. It also shows the plugin tree.

## The model

An agent harness is everything in an agent except the model. Agent = Model + Harness.

The skill builds the outer harness for one code project. The outer harness has two kinds of control:

- Guides. Feedforward controls. A guide steers the agent before it acts. Examples: `AGENTS.md`, skills, bootstrap scripts.
- Sensors. Feedback controls. A sensor observes the agent after it acts. The agent uses the sensor output to self-correct. Examples: tests, linters, type checkers, AI review.

Use both kinds. A harness with only sensors repeats the same mistakes. A harness with only guides never finds out whether its rules work.

Each guide and sensor is one of two types:

- Computational. Deterministic and fast. Examples: tests, linters, type checkers.
- Inferential. Semantic and slower. Examples: AI code review, an LLM as judge.

Write sensor output for the model. A check that fails tells the agent how to fix the problem.

Put checks early. Fast checks run before a commit. Slow checks run later.

The steering loop: when an issue happens more than once, improve the guides or sensors. The human steers the harness.

## The plugin as harness

The plugin packages the harness as one Agent Plugins 1.0 plugin. Each part of the plugin maps to a harness role (see the table below).

## Mapping: harness part to file

| Harness part | Role | Claude Code | Copilot CLI | Location |
| --- | --- | --- | --- | --- |
| Skills | guide | `skills/` | `skills/` | Plugin, portable |
| MCP servers | guide tool, optional | `.mcp.json` | `mcp.json` | Plugin, portable |
| Reviewer agent | inferential sensor | `agents/<agent>.md` | `com.github.copilot/agents/<agent>.agent.md` | Plugin, client-specific |
| Skill evals | test for the guide | `skills/<skill>/evals/` | Same | Plugin, inside `skills/` |
| MCP check | computational sensor for the MCP files | `scripts/check-mcp.py` | Same | Plugin repo, not a component |
| Plugin evals | test for the harness | `evals/` (`claude plugin eval`) | None | Plugin repo, not a component |
| Steering loop | process | None | None | `CHANGELOG.md` in the plugin root |

## Plugin tree

This is the tree of the plugin that the skill generates today. Each part has a harness role. `packaging` marks parts with no harness role.

```txt
<plugin-name>/
├── plugin.json                        # packaging: Agent Plugins 1.0 manifest
├── .claude-plugin/
│   ├── plugin.json                    # packaging: Claude Code manifest
│   └── marketplace.json               # packaging: marketplace catalog
│
├── skills/                            # both formats read this folder
│   └── <skill-name>/                  # folder name = `name` in SKILL.md
│       ├── SKILL.md                   # guide: instructions for the agent, under 500 lines
│       ├── scripts/
│       │   └── <script-name>.py       # script the skill runs: shebang, --help, JSON output
│       ├── references/
│       │   ├── role.md                # source text for the reviewer agent body
│       │   └── <topic>.md             # guide: read only when the skill needs it
│       ├── assets/                    # guide: templates and static files
│       │   └── <template>.md
│       └── evals/                     # sensor for the skill: Agent Skills format
│           ├── evals.json             # test cases
│           ├── train_queries.json     # trigger queries, used to tune the description
│           ├── validation_queries.json # different queries, used to check the description
│           └── files/                 # input files for the test cases
│               └── <input-file>
│
├── agents/                            # inferential sensor: Claude Code reviewer agents
│   └── <agent-name>.md                # frontmatter + body from role.md
├── com.github.copilot/                # Copilot-only files
│   └── agents/
│       └── <agent-name>.agent.md      # inferential sensor: frontmatter + body from role.md
├── mcp.json                           # guide tool: Agent Plugins MCP file, optional
├── .mcp.json                          # guide tool: Claude Code MCP file, optional
├── servers/                           # only for a server that you write
│   ├── <server-name>.py               # MCP server: SDK 2.x, PEP 723 header
│   └── <server-name>.py.lock          # from `uv lock --script`
│
├── evals/                             # sensor for the harness: claude plugin eval format
│   ├── <skill-name>-task/
│   │   ├── prompt.md                  # request, as a user types it
│   │   ├── case.yaml                  # case settings
│   │   ├── fixture.sh                 # Bash script, creates the input files
│   │   └── graders/
│   │       ├── criteria.md            # llm grader, gives the score
│   │       └── skill-fired.md         # indicator: did the skill start
│   ├── unrelated-request/             # negative control
│   │   ├── prompt.md
│   │   └── graders/
│   │       └── no-skill.md            # passes if no skill starts
│   └── results/                       # output of each run, not part of the harness
│
├── scripts/
│   ├── sync-agents.py                 # build step: copies role.md into agent bodies; --check finds drift
│   └── check-mcp.py                   # sensor: MCP servers on both protocol eras; mcp.json vs .mcp.json drift
├── .gitignore                         # packaging: evals/results/ and .workspace/
├── README.md                          # documentation for people
├── CHANGELOG.md                       # steering loop: one entry for each release
└── LICENSE                            # packaging
```

Each client reads these paths:

- Agent Plugins clients and Copilot read `plugin.json`, `skills/`, `mcp.json`, and `com.github.copilot/`.
- Claude Code reads `.claude-plugin/`, `skills/`, `agents/`, and `.mcp.json`.
- Both clients read `.claude-plugin/marketplace.json`.
- Cursor and Codex read the root `plugin.json` and `skills/`. Both also read `AGENTS.md`.
- Cursor and Codex read `mcp.json`. Cursor does not replace `${PLUGIN_ROOT}` in it. No Codex document confirms the replacement.
- Cursor reads agents from `.cursor/agents/`. Codex reads only TOML agents from `.codex/agents/`. A plugin does not carry them.
- Codex reads its marketplace from `.agents/plugins/marketplace.json`.
- The skill generates none of the Cursor and Codex files in the last three items. It supports the skills of the plugin in Cursor and Codex.

In the tree, `<skill-name>` is the name of one skill. Repeat the folder for each skill. `<agent-name>` is the name of one agent. `<script-name>`, `<server-name>`, and `<topic>` are names that you choose.
