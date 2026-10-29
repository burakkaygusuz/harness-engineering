# Sources

The skill follows these official documents.

## Agent Skills and Agent Plugins

- Agent Skills specification: `https://agentskills.io/specification`
- Agent Skills client guide: `https://agentskills.io/client-implementation/adding-skills-support`
- Agent Skills script guide: `https://agentskills.io/skill-creation/using-scripts`
- Agent Skills eval guide: `https://agentskills.io/skill-creation/evaluating-skills`
- Agent Skills best practices: `https://agentskills.io/skill-creation/best-practices`
- Agent Skills description guide: `https://agentskills.io/skill-creation/optimizing-descriptions`
- skills-ref validator (allowed frontmatter fields): `https://github.com/agentskills/agentskills/blob/main/skills-ref/src/skills_ref/validator.py`
- Agent Plugins specification 1.0: `https://agent-plugins.org/specification`
- Agent Plugins schema 1.0.0: `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`
- Agent Plugins MCP schema 1.0.0: `https://agent-plugins.org/schemas/1.0.0/mcp.schema.json`
- Agent Plugins example: `https://github.com/agentplugins/agent-plugins-example`

## Claude Code

- Claude Code plugin guide: `https://code.claude.com/docs/en/plugins/create`
- Claude Code plugin components: `https://code.claude.com/docs/en/plugins/components`
- Claude Code plugin dependencies: `https://code.claude.com/docs/en/plugins/dependencies`
- Claude Code plugin measure page: `https://code.claude.com/docs/en/plugins/measure`
- Claude Code example plugin: `https://github.com/anthropics/claude-plugins-official/tree/main/plugins/example-plugin`
- Claude Code plugin reference: `https://code.claude.com/docs/en/plugins-reference`
- Claude MCP (client runtimes, plugin servers): `https://code.claude.com/docs/en/mcp`
- Claude Code plugin eval page: `https://code.claude.com/docs/en/plugin-evals`
- Claude Code marketplace reference: `https://code.claude.com/docs/en/plugins/marketplace-reference`
- Claude Code publish page: `https://code.claude.com/docs/en/plugins/publish`
- Claude subagents (agent file fields, `model`): `https://code.claude.com/docs/en/sub-agents`
- Claude memory (`CLAUDE.md`, `AGENTS.md`, imports): `https://code.claude.com/docs/en/memory`
- Claude hooks: `https://code.claude.com/docs/en/hooks`
- Claude settings: `https://code.claude.com/docs/en/settings`
- Claude features overview: `https://code.claude.com/docs/en/features-overview`

## GitHub Copilot

- GitHub Copilot CLI plugin reference: `https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference`
- GitHub Copilot custom agents configuration (agent file fields, `model`): `https://docs.github.com/en/copilot/reference/custom-agents-configuration`
- GitHub Copilot CLI custom agents (subagents and project instructions): `https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli`
- GitHub Copilot hooks reference: `https://docs.github.com/en/copilot/reference/hooks-reference`
- GitHub Copilot custom instructions (`AGENTS.md`, `CLAUDE.md`): `https://docs.github.com/en/copilot/concepts/prompting-and-context/custom-instructions`
- GitHub Copilot custom instructions support (which client reads which file): `https://docs.github.com/en/copilot/reference/custom-instructions-support`
- GitHub Copilot CLI release 1.0.81 (2026-07-28 protocol support): `https://github.com/github/copilot-cli/releases/tag/v1.0.81`

## VS Code

- VS Code agent plugins page: `https://code.visualstudio.com/docs/agent-customization/agent-plugins`
- VS Code agent plugin reference (formats, `${PLUGIN_ROOT}`): `https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference`
- VS Code custom agents page: `https://code.visualstudio.com/docs/agent-customization/custom-agents`
- VS Code subagents page: `https://code.visualstudio.com/docs/agents/run/subagents`
- VS Code custom agent file reference (`model`, `model-policy`): `https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference`

## Model Context Protocol

- MCP versioning (2026-07-28): `https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning.md`
- MCP stdio transport (2026-07-28): `https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio.md`
- MCP deprecated features (2026-07-28): `https://modelcontextprotocol.io/specification/2026-07-28/deprecated.md`
- MCP changelog (2026-07-28): `https://modelcontextprotocol.io/specification/2026-07-28/changelog.md`
- MCP build a server (2026-07-28): `https://modelcontextprotocol.io/docs/2026-07-28/develop/build-server.md`
- MCP Inspector CLI (2026-07-28): `https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector/cli.md`
- MCP Inspector protocol eras (2026-07-28): `https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector/protocol-eras.md`
- MCP Inspector configuration (2026-07-28): `https://modelcontextprotocol.io/docs/2026-07-28/tools/inspector/configuration.md`
- MCP Inspector 2.13.0 release notes: `https://github.com/modelcontextprotocol/inspector/releases/tag/2.13.0`
- MCP Inspector advisory (three advisories, fixed in 2.12.0): `https://github.com/modelcontextprotocol/inspector/security/advisories/GHSA-q978-78c7-phqw`, `https://github.com/modelcontextprotocol/inspector/security/advisories/GHSA-vcc9-3xgm-p9v4`, `https://github.com/modelcontextprotocol/inspector/security/advisories/GHSA-m5pj-3536-3xcp`
- MCP Python SDK protocol versions: `https://py.sdk.modelcontextprotocol.io/protocol-versions/`
- MCP Python SDK legacy clients: `https://py.sdk.modelcontextprotocol.io/run/legacy-clients/`

## Python

- Python versions (support status, end of life): `https://devguide.python.org/versions/`
- uv scripts guide (PEP 723, `--script`, lock files): `https://docs.astral.sh/uv/guides/scripts/`
- uv CLI reference: `https://docs.astral.sh/uv/reference/cli/`

## Harness engineering

Three rules apply to this section:

- A design rule in this skill needs two or more independent Tier 1 or Tier 2 sources. A rule with only one source says so in its text.
- The model terms come from Böckeler: harness, guide, sensor, computational, inferential, and steering loop. A definition needs one source.
- File formats and client behavior come only from the official documents in the sections above.

### Tier 1: first-party engineering posts and formats

- OpenAI, "Harness engineering: leveraging Codex in an agent-first world" (2026-02-11): `https://openai.com/index/harness-engineering/`
- Anthropic, "Effective harnesses for long-running agents" (2025-11-26): `https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents`
- Anthropic, "Harness design for long-running application development" (2026-03-24): `https://www.anthropic.com/engineering/harness-design-long-running-apps`
- Anthropic, "Demystifying evals for AI agents" (2026-01-09): `https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents`
- LangChain, "Improving Deep Agents with harness engineering" (2026-02-17): `https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering`
- Cursor, "Continually improving our agent harness" (2026-04-30): `https://cursor.com/blog/continually-improving-agent-harness`
- Anthropic, "Writing effective tools for AI agents" (2025-09-11): `https://www.anthropic.com/engineering/writing-tools-for-agents`
- Anthropic, "Code execution with MCP for efficient agents" (2025-11-04): `https://www.anthropic.com/engineering/code-execution-with-mcp`
- AGENTS.md format (Agentic AI Foundation, Linux Foundation): `https://agents.md/`

### Tier 2: recognized practitioners

- Böckeler, "Harness engineering for coding agent users" (2026-04-02): `https://martinfowler.com/articles/harness-engineering.html`
- Hashimoto, "My AI Adoption Journey" (2026-02-05): `https://mitchellh.com/writing/my-ai-adoption-journey`. The earliest exact-phrase use of "harness engineering" that was found. The post does not claim to coin the term.

### Tier 3: reading list

No claim in the skill rests on these sources.

- `https://github.com/walkinglabs/learn-harness-engineering`
- `https://github.com/walkinglabs/awesome-harness-engineering`
