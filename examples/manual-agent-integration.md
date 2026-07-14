# Manual integration example

For an agent without native Agent Skills discovery, expose only skill metadata
at startup:

```xml
<available_skills>
  <skill>
    <name>content-grounding</name>
    <description>Copy the description from the skill frontmatter.</description>
    <path>/absolute/path/skills/content-grounding/SKILL.md</path>
  </skill>
</available_skills>
```

When a request matches:

1. read only the selected `SKILL.md`;
2. follow its instructions;
3. load referenced files only when required;
4. run deterministic scripts with explicit local paths;
5. retain observed, measured, inferred, and unknown evidence labels;
6. never treat an aesthetic pattern as proof of AI authorship.

Use `manifest.json` as the complete skill index. Broad requests may activate
`anti-ai-slop`; narrow requests should activate the focused skill directly.
