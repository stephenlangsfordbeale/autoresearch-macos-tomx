# Autoresearch User Guide

This repository has two complementary ways to work: the local dashboard for
guided operations, and the command line for direct control.

## Start with the dashboard

From the repository root:

```bash
./autoresearch-dashboard
```

The dashboard opens a local browser page with two profiles:

- **Autoresearch MacOS** — the local `train.py` loop using the fixed five-minute
  budget and `val_bpb` as the keep/discard metric.
- **ToMX Local Quality** — the external Theory-of-Mind benchmark workspace,
  using its train/evaluate/select workflow and ToM-specific gate rules.

Use **Refresh Status** before starting work. The status panel reports the
selected workspace, branch, required files, interpreter readiness, and whether
Codex is available.

## Send a prompt to Codex

Choose a profile, select an agent or suggestion, adjust the focus text, and
press **Send To Codex**. The dashboard starts a managed, non-interactive
`codex exec` job in that profile’s workspace. It does not use clipboard,
AppleScript, or GUI keystrokes.

Prompt jobs write JSONL logs under:

```text
.omx/state/dashboard-codex/
```

The dashboard transcript and current job panel show the job status and working
directory. Use **Stop Current Job** when a running prompt or training action
needs to be terminated.

## Run experiments

For the local autoresearch profile, the useful actions are:

- **Ensure results.tsv** — creates the expected results header if needed.
- **Create Run Branch** — creates an `autoresearch/<tag>` branch.
- **Run Baseline Train** — launches the bounded local training command.

For the ToMX profile:

- **Run Smoke Then Gate** — runs a short smoke check, then the 800-episode gate
  if the smoke succeeds.
- **Run 3-Seed Quick Gate** — runs the configured ToMX quick-gate seed set.

Training actions are real experiments. Review the selected workspace and output
label before launching them.

## Direct command-line work

Use the regular Codex CLI when you want direct control:

```bash
codex exec -C /path/to/repository -
```

Use `omx` when you explicitly need orchestration features such as setup,
autoresearch supervision, HUD/state management, teams, or Ralph workflows:

```bash
./omx doctor
./omx setup --scope project --force --verbose
./omx autoresearch --help
```

`omx` and `codex` are complementary commands; `omx` is not a replacement for
the regular Codex CLI.

## Configuration

Codex discovery uses the first available option in this order:

1. `AUTORESEARCH_CODEX_CLI`
2. `CODEX_CLI_PATH`
3. `codex` on `PATH`
4. `/Applications/ChatGPT.app/Contents/Resources/codex`

The ToMX profile can be relocated or pointed at alternate support files with:

```bash
export AUTORESEARCH_TOMX_ROOT=/path/to/ToM_AI_Research_Team
export AUTORESEARCH_TOMX_PYTHON=/path/to/python
export AUTORESEARCH_TOMX_TASK_PATH=/path/to/OMX_TASK.md
export AUTORESEARCH_TOMX_SKILL_PATH=/path/to/tomx/SKILL.md
```

The defaults preserve the current local checkout layout.

## Troubleshooting

Run the lightweight checks first:

```bash
python .codex/skills/autoresearch-lab/scripts/autoresearch_ops.py check-setup --json --repo-only
./autoresearch-dashboard --help
./omx doctor
```

If Codex is not found, set `AUTORESEARCH_CODEX_CLI` or `CODEX_CLI_PATH` to an
executable Codex CLI path. If a ToMX profile is not ready, check its configured
root, Python interpreter, `OMX_TASK.md`, `train.py`, runner, and agent directory.
