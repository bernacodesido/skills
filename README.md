# bernacodesido/skills

A collection of Claude skills — reusable instruction packages that teach Claude how to handle specific tasks and workflows consistently across Claude.ai, Claude Code, and the API.

## Contents

- [What is a skill?](#what-is-a-skill)
- [Repository structure](#repository-structure)
- [Creating a new skill](#creating-a-new-skill)
- [SKILL.md reference](#skillmd-reference)
- [Writing effective instructions](#writing-effective-instructions)
- [Skill categories](#skill-categories)
- [Installing a skill](#installing-a-skill)
- [Development setup](#development-setup)
- [Validation](#validation)

---

## What is a skill?

A skill is a folder that teaches Claude how to handle a specific task or workflow. Instead of re-explaining your processes in every conversation, you define them once and Claude applies them consistently every time.

A skill folder contains:

| Path | Required | Purpose |
|---|---|---|
| `SKILL.md` | Yes | Instructions in Markdown with YAML frontmatter |
| `scripts/` | No | Executable code (Python, Bash, etc.) |
| `references/` | No | Documentation Claude loads on demand |
| `assets/` | No | Templates, fonts, icons used in output |

### How Claude loads a skill (progressive disclosure)

Skills use a three-level loading system to minimise token usage:

1. **YAML frontmatter** — always loaded in Claude's system prompt; used to decide whether the skill is relevant
2. **SKILL.md body** — loaded when Claude determines the skill applies to the current task
3. **Linked files in `references/` and `assets/`** — loaded only when Claude needs the specific detail

---

## Repository structure

```
skills/
├── README.md               ← human-facing docs (never goes inside a skill folder)
├── _template/              ← copy this to start a new skill
│   ├── SKILL.md
│   ├── scripts/
│   ├── references/
│   └── assets/
├── .pre-commit-config.yaml ← runs the validator before every commit
└── .github/
    ├── workflows/
    │   └── validate-skills.yml   ← CI validation on push and PRs
    └── scripts/
        └── validate_skills.py    ← shared validation logic
```

Each skill lives in its own top-level folder:

```
your-skill-name/
├── SKILL.md
├── scripts/        ← optional
│   └── process.py
├── references/     ← optional
│   └── api-guide.md
└── assets/         ← optional
    └── template.md
```

---

## Creating a new skill

1. Copy `_template/` and rename it using kebab-case — e.g. `sprint-planner`
2. Open `SKILL.md` and fill in the frontmatter `name` and `description` first (see [SKILL.md reference](#skillmd-reference))
3. Write the instructions in the body (see [Writing effective instructions](#writing-effective-instructions))
4. Delete any optional subdirectories (`scripts/`, `references/`, `assets/`) you don't need
5. Run `pre-commit run --all-files` to validate before committing
6. Install the skill to test it (see [Installing a skill](#installing-a-skill))

---

## SKILL.md reference

Every skill must contain a file named exactly `SKILL.md` (case-sensitive). It starts with YAML frontmatter, followed by the instruction body in Markdown.

### Frontmatter fields

```yaml
---
name: your-skill-name          # required — see rules below
description: >                 # required — see rules below
  What it does. Use when user asks to [task], says "[phrase]",
  or mentions "[keyword]". Key capabilities: [A], [B], [C].
license: MIT                   # optional — use if open-sourcing
compatibility: Works with Claude.ai, Claude Code, and the API.  # optional, 1–500 chars
metadata:                      # optional — any key-value pairs
  author: Your Name
  version: 1.0.0
  mcp-server: your-server-name
---
```

#### `name` (required)

- Must be kebab-case: lowercase letters and hyphens only
- No spaces, underscores, or capitals
- Must exactly match the folder name
- Must not contain `claude` or `anthropic` (reserved)

```
sprint-planner   ✓
Sprint Planner   ✗  (capitals and spaces)
sprint_planner   ✗  (underscores)
SprintPlanner    ✗  (capitals)
```

#### `description` (required)

This is the most important field — it is what Claude reads to decide whether to load the skill at all. Get it right.

- Must include **what the skill does** and **when to use it** (trigger conditions)
- Under 1024 characters
- No XML angle brackets (`<` or `>`)
- Include specific phrases users might say

Structure: `[What it does] + [When to use it] + [Key capabilities]`

```yaml
# Good — specific, includes trigger phrases
description: >
  Generates frontend designs from specs with high design quality.
  Use when user asks for "design specs", "component documentation",
  or "design-to-code handoff". Works with Figma files.

# Bad — too vague, no trigger conditions
description: Helps with projects.

# Bad — technical, no user-facing triggers
description: Implements the Project entity model with hierarchical relationships.
```

#### Security restrictions

The frontmatter is injected into Claude's system prompt. Never include:
- XML angle brackets (`<` or `>`) anywhere in frontmatter
- `claude` or `anthropic` in the skill `name`

### SKILL.md body structure

After the frontmatter, write the instructions in Markdown. Recommended structure:

```markdown
# Skill Name

## Instructions

### Step 1: [First major step]
Clear, specific explanation. Include exact commands where relevant.

```bash
python scripts/process.py --input {filename}
Expected output: [describe what success looks like]
```

### Step 2: [Second major step]
...

## Examples

### Example 1: [Common scenario]
User says: "[trigger phrase]"
Actions:
1. [First action]
2. [Second action]
Result: [Expected outcome]

## Common Issues

### Error: [Error message]
**Cause:** [Why it happens]
**Solution:** [How to fix]
```

### Referencing other files

Keep `SKILL.md` focused on core instructions. Move detailed documentation to `references/` and link to it:

```markdown
Before writing queries, consult `references/api-patterns.md` for:
- Rate limiting guidance
- Pagination patterns
- Error codes and handling
```

---

## Writing effective instructions

### Be specific and actionable

```
# Good
Run `python scripts/validate.py --input {filename}` to check data format.
If validation fails, common issues include:
- Missing required fields (add them to the CSV)
- Invalid date formats (use YYYY-MM-DD)

# Bad
Validate the data before proceeding.
```

### Include error handling

Document what Claude should do when things go wrong, especially for MCP connections:

```markdown
## Common Issues

### MCP Connection Failed
If you see "Connection refused":
1. Verify MCP server is running: Settings > Extensions
2. Confirm API key is valid
3. Try reconnecting: Settings > Extensions > [Service] > Reconnect
```

### Use progressive disclosure

Keep `SKILL.md` focused on the core workflow. Move reference material to `references/` so it is only loaded when needed, reducing token usage.

---

## Skill categories

Based on Anthropic's guide, skills fall into three categories:

### Category 1: Document & Asset Creation

Creating consistent, high-quality output — documents, presentations, designs, code.

Key techniques:
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalising
- No external tools required (uses Claude's built-in capabilities)

### Category 2: Workflow Automation

Multi-step processes that benefit from consistent methodology, including coordination across multiple MCP servers.

Key techniques:
- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

### Category 3: MCP Enhancement

Workflow guidance layered on top of an MCP server's tool access.

Key techniques:
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

---

## Installing a skill

**Claude Code** — place the skill folder in your Claude Code skills directory.

**Claude.ai** — Settings › Capabilities › Skills › Upload skill (zip the folder first if needed).

**API / Agent SDK** — add skills to Messages API requests via the `container.skills` parameter. Requires the Code Execution Tool beta.

Skills are portable: a skill built once works identically across all three surfaces.

---

## Development setup

Install the pre-commit hook so the validator runs automatically before every commit:

```bash
pip install -r requirements.txt
pip install pre-commit
pre-commit install
```

To run the validator manually at any time:

```bash
python .github/scripts/validate_skills.py
```

The same validation runs in CI on every push and pull request via the GitHub Actions workflow at [`.github/workflows/validate-skills.yml`](.github/workflows/validate-skills.yml).

---

## Validation

The validator ([`.github/scripts/validate_skills.py`](.github/scripts/validate_skills.py)) checks every top-level skill folder (excluding `_template` and hidden directories). It enforces the following rules:

### Errors (block merge)

| Rule | Detail |
|---|---|
| Folder name is kebab-case | Lowercase letters and hyphens only |
| Folder name has no reserved words | Must not contain `claude` or `anthropic` |
| `SKILL.md` exists | Case-sensitive — `skill.md` and `SKILL.MD` are rejected |
| No `README.md` in skill folder | Docs belong in `SKILL.md` or `references/` |
| Frontmatter is valid YAML | Must be present and parseable |
| No XML angle brackets in frontmatter | `<` and `>` are forbidden everywhere in frontmatter |
| `name` is present and kebab-case | Required field |
| `name` matches the folder name | Must be identical |
| `description` is present | Required field |
| `description` is under 1024 characters | Hard limit |
| `description` has no XML angle brackets | `<` and `>` are forbidden |
| `compatibility` is 1–500 chars (if present) | Optional field length bounds |

### Warnings (informational, do not block merge)

| Rule | Detail |
|---|---|
| `description` includes trigger conditions | Should contain "use when", "when user", or "when the user" |
| Body has `## Instructions` section | Recommended structure |
