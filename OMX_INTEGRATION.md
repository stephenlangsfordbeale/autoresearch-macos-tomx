# oh-my-codex integration

This repo has a repo-local oh-my-codex source checkout at:

- `./oh-my-codex`

It has been built locally and installed in **project scope** for this repository.

Project-local OMX surfaces now live at:
- `./.codex/`
- `./.omx/`
- `./AGENTS.md`

## Recommended local launcher

Use the repo-local wrapper from the repo root:

```bash
./omx doctor
./omx setup --scope project --force --verbose
./omx explore --help
```

The wrapper resolves to:
- `node ./oh-my-codex/dist/cli/omx.js`

## Notes

- This integration is local to this repo checkout.
- The project-scope install keeps OMX config under this repository instead of your user-wide Codex directories.
- `omx` is the orchestration/runtime launcher; the autoresearch dashboard uses the regular `codex exec` CLI for prompt delivery.
- Dashboard Codex discovery is configurable with `AUTORESEARCH_CODEX_CLI` or `CODEX_CLI_PATH`; it does not depend on a `Codex.app` GUI bundle.
- If `oh-my-codex` source is updated, rebuild it with:

```bash
cd oh-my-codex
npm install
npm run build
```

Then rerun project setup if needed:

```bash
cd ..
./omx setup --scope project --force --verbose
```
