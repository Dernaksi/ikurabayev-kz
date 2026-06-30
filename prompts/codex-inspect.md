# Codex Inspect Prompt

Use this prompt before implementation.

```text
Inspect this repository for the requested IKurabayev.kz task.

Rules:
- Do not modify files.
- Read AGENTS.md, README.md, relevant docs, issue context, and relevant files.
- Do not add dependencies or website implementation.
- Do not read or expose secrets, private credentials, .env files, contracts, or
  unpublished research data.
- Report evidence-based findings only.

Return:
1. Files inspected.
2. Current repository state.
3. Relevant constraints.
4. Proposed files to change.
5. Risks, missing sources, or questions.
```

