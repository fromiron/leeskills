# Integration

## Generic Agent Skills client

Register each directory under `skills/` with a client that supports the open
Agent Skills format. The client should initially expose only each skill's
`name`, `description`, and path, then load `SKILL.md` on activation.

For clients without native discovery, `manifest.json` provides an index.

## Manual system-prompt integration

A simple implementation can enumerate skills like this:

```xml
<available_skills>
  <skill>
    <name>content-grounding</name>
    <description>...</description>
    <path>/absolute/path/skills/content-grounding/SKILL.md</path>
  </skill>
</available_skills>
```

On a match:

1. read the selected `SKILL.md`;
2. follow the workflow;
3. read referenced files only when their trigger condition applies;
4. run optional scripts only with explicit, scoped file paths;
5. preserve evidence labels in the final output.

## OpenAI Codex

Repository-scoped skills belong under:

```text
<repo>/.agents/skills/
```

User-scoped skills belong under:

```text
~/.agents/skills/
```

Use the installer or copy the individual skill directories. See
`adapters/codex/README.md`.

## Claude Code

Repository-scoped skills belong under:

```text
<repo>/.claude/skills/
```

User-scoped skills belong under:

```text
~/.claude/skills/
```

Use the installer or copy the individual skill directories. See
`adapters/claude-code/README.md`.

## Invocation strategy

The orchestrator is useful for broad requests such as:

- audit this landing page for generic AI design;
- simplify this portfolio without losing necessary information;
- review this generated UI and remove unsupported content;
- define a minimal, accessible structure from these source materials.

Use focused skills for narrower requests. Avoid loading the full suite when a
copy-only or motion-only task needs two or three skills.

## Multilingual content

The instructions are written in English for broad client compatibility.
Outputs should preserve the language of the user's artifact unless the user
requests translation. Phrase watchlists include English, Korean, and Japanese,
but matches are warnings rather than automatic failures.
