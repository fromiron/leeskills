# Security policy

## Trust model

Agent skills are executable operational text. Review every `SKILL.md`, script,
reference, and asset before installing a third-party fork.

This repository follows these constraints:

- bundled Python scripts use only the standard library;
- scripts do not make network requests;
- scripts do not read outside paths explicitly supplied by the caller;
- scripts do not mutate product files unless an explicit output path is given;
- install operations refuse to overwrite an existing skill unless `--force`
  is supplied;
- no skill receives pre-approved tools through `allowed-tools`.

## Reporting

Report suspected prompt injection, data exfiltration, unsafe file access,
dependency confusion, or misleading provenance through the repository's
private security reporting channel.

Do not include secrets, private customer artifacts, or unpublished designs in
a public report.

## Safe review checklist

1. Read all frontmatter and instructions.
2. Inspect every referenced file.
3. Run `python scripts/validate_repo.py`.
4. Search scripts for network, process, and destructive filesystem operations.
5. Test in a disposable repository before user-wide installation.
