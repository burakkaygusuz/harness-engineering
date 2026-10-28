# Agent harness

This file explains the harness model. It maps each harness part to a file in the plugin. It also shows the plugin tree.

## The model

An agent harness is everything in an agent except the model. Agent = Model + Harness. [Böckeler]

The skill builds the outer harness for one code project. The outer harness has two kinds of control:

- Guides. Feedforward controls. A guide steers the agent before it acts. Examples: `AGENTS.md`, skills, bootstrap scripts. [Böckeler]
- Sensors. Feedback controls. A sensor observes the agent after it acts. The agent uses the sensor output to self-correct. Examples: tests, linters, type checkers, AI review. [Böckeler]

Use both kinds. A harness with only sensors repeats the same mistakes. A harness with only guides never finds out whether its rules work. This rule has one source. [Böckeler]

Each guide and sensor is one of two types:

- Computational. Deterministic and fast. Examples: tests, linters, type checkers. [Böckeler]
- Inferential. Semantic and slower. Examples: AI code review, an LLM as judge. [Böckeler]

Write sensor output for the model. A failing check tells the agent how to fix the problem. [OpenAI] [Böckeler]

Put checks early. Fast checks run before a commit. Slow checks run later. This rule has one source. [Böckeler]

The steering loop: when an issue happens more than once, improve the guides or sensors. The human steers the harness. [Böckeler] [OpenAI]

## The plugin as harness

This interpretation is ours. The plugin packages the harness as one Agent Plugins 1.0 plugin. Each part of the plugin maps to a harness role (see the table below). Böckeler describes "harness templates" as a possible future form: "a bundle of guides and sensors that leash a coding agent to the structure, conventions and tech stack of a topology." [Böckeler]

## Mapping: harness part to file

| Harness part | Role | Claude Code | Copilot CLI | Location |
| --- | --- | --- | --- | --- |
| Skills | guide | `skills/` | `skills/` | Plugin, portable |
| MCP tools | guide or sensor | `.mcp.json` | `mcp.json` | Plugin, portable |
| Reviewer agent | inferential sensor | `agents/<agent>.md` | `com.github.copilot/agents/<agent>.agent.md` | Plugin, client-specific |
| Skill evals | test for the guide | `skills/<skill>/evals/` | Same | Plugin, inside `skills/` |
| Plugin evals | test for the harness | `evals/` (`claude plugin eval`) | None | Plugin repo, not a component |
| Steering loop | process | None | None | `CHANGELOG.md` in the plugin root |

Notes:

- Plugin agents cannot define `hooks`, `mcpServers`, or `permissionMode`. Client-specific agent files carry that configuration. [Claude Code plugin reference]
- Copilot CLI reads its client-specific files from `com.github.copilot/`. [GitHub Copilot CLI plugin reference]
- Claude Code reads `.claude-plugin/`, `agents/`, and `.mcp.json`. [Claude Code plugin reference]

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
│       │   └── <script-name>.mjs      # script the skill runs: shebang, --help, JSON output
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
├── mcp.json                           # guide or sensor: Agent Plugins MCP file, optional
├── .mcp.json                          # guide or sensor: Claude Code MCP file, optional
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
│   └── sync-agents.sh                 # build step: copies role.md into agent bodies; --check finds drift
├── .gitignore                         # packaging: evals/results/ and .workspace/
├── README.md                          # documentation for people
├── CHANGELOG.md                       # steering loop: one entry for each release
└── LICENSE                            # packaging
```

Each client reads these paths:

- Agent Plugins clients and Copilot read `plugin.json`, `skills/`, `mcp.json`, and `com.github.copilot/`.
- Claude Code reads `.claude-plugin/`, `skills/`, `agents/`, and `.mcp.json`.
- Both clients read `.claude-plugin/marketplace.json`.
- The `evals/` folder at the root is for `claude plugin eval`. The folders `skills/<skill-name>/evals/` are for the Agent Skills eval format. The two eval systems use different file formats.

In the tree, `<skill-name>` is the name of one skill. Repeat the folder for each skill. `<agent-name>` is the name of one agent. `<script-name>` and `<topic>` are names that you choose.

The scripts use Node.js 22.12 or later. The project has no Python code and no packages.
