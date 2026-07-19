# Vendored workflow steps

These six step directories (`align`, `continue`, `handoff`, `next-issue`,
`plan-issues`, `ship`) are **vendored copies**. The source of truth is
[coding-agent-toolkit](https://github.com/stefan-jansen/coding-agent-toolkit)
(`skills/<step>/`).

Do not edit them here. Edit the step in the toolkit, then re-vendor:

```bash
scripts/sync-from-toolkit.sh          # copy toolkit -> here
scripts/sync-from-toolkit.sh --check  # verify in sync (pre-commit runs this)
```

They are committed as real files, not symlinks, so this marketplace stays
self-contained when cloned without the toolkit present.
