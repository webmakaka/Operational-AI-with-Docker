# 03 — Long syntax with custom env var names

The long syntax lets you override the default variable names Compose injects.

This is useful when:
- Your app already uses `LLM_URL` for a different purpose.
- You want more descriptive variable names for a large multi-model app.
- You're migrating from an existing env-var schema.

The functionality is identical to short syntax — only the injected variable
names change.
