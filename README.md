# autoresearch-macos-tomx

A lightweight research orchestration toolkit for disciplined single-file autoresearch loops on macOS using Codex + oh-my-codex (OMX).

This repository provides task contracts, seed-gate policies, promotion rules, runner templates, backend adapters, and reporting scaffolds that sit beside — not inside — a benchmark repository.

It is designed for workflows where:

- only one file is editable (e.g. `train.py`)
- benchmark semantics are frozen
- evaluation seeds are fixed
- promotion decisions are policy-driven
- artifacts are part of the scientific record
- autonomous patch loops must remain reproducible

The benchmark repo remains the scientific source of truth. This repo provides orchestration.

---

## Repository Purpose

This project implements a reusable “single-surface autoresearch loop”:

1. Edit a constrained file
2. Run fixed-budget evaluation
3. Compare against baseline
4. Apply promotion rules
5. Keep or discard the patch
6. Repeat

Typical targets:

- policy-learning loops
- belief-state heuristics
- solver hyperparameters
- auxiliary losses
- decision priors
- interpretability heuristics

---

## Design Principles

This toolkit enforces:

- frozen benchmark semantics
- explicit promotion thresholds
- seed-set comparability
- artifact contracts
- provenance tracking
- reproducible evaluation ladders

It deliberately avoids:

- modifying benchmark environments
- redefining metrics implicitly
- mixing workflow logic into science repos
- uncontrolled multi-file edits
- silent evaluation drift

---

## Intended Workflow

Example loop:

```
edit train.py
run smoke validation
run quick gate (3 seeds)
run promotion gate (5 seeds)
compare metrics
promote or reject
archive artifacts
repeat
```

This repository provides templates and policies for each stage.

---

## Repository Layout

autoresearch-macos-tomx/
├── README.md
├── docs/
├── task_policies/
├── agents/
├── policies/
├── templates/
├── runners/
├── backends/
├── examples/
└── scripts/

See `docs/architecture.md` for details.

---

## Quick Start

### 1. Clone
```
python scripts/local_runner.py 
–train-episodes 5 
–seed 7 
–output-root logs/smoke_checkgit clone 
cd autoresearch-macos-tomx
```

---

### 2. Attach to benchmark repo

Edit:
```
examples/tom_ai_research_team/repo_overlay.yaml
```

Set:

- canonical repo root
- safe edit surface
- frozen files
- runner commands
- artifact paths

---

### 3. Verify benchmark still runs

Example smoke command:
```
python scripts/local_runner.py 
–train-episodes 5 
–seed 7 
–output-root logs/smoke_check
```

Smoke confirms harness integrity only.

It does not support promotion decisions.

---

### 4. Run quick gate
```
python scripts/local_runner.py 
–train-episodes 800 
–seed 7 
–output-root logs/exp_seed7
```

Repeat for:
11
17

---

### 5. Run promotion gate

Add:
23
29
```
Promotion requires passing all gate rules.
```
---

## Promotion Criteria (Default)

Across 5 seeds:
```
- mean DeadlockRate not worse
- mean ToMCoordScore higher
- mean CollisionRate lower or equal
- mean SuccessRate higher or equal
- no catastrophic single-seed regression
```
Catastrophic regression example:

---

## Promotion Criteria (Default)

Across 5 seeds:

- mean DeadlockRate not worse
- mean ToMCoordScore higher
- mean CollisionRate lower or equal
- mean SuccessRate higher or equal
- no catastrophic single-seed regression

Catastrophic regression example:
DeadlockRate delta > +0.10

---

## Supported Execution Backends

Adapters exist for:

- Codex CLI
- local Python runner
- Modal continuation workflows

Optional:

- Azure compatibility wrappers

---

## OMX Integration

This repo assumes project-local OMX installation.

Recommended commands:
```
./omx doctor
./omx setup –scope project –force –verbose
```
OMX is used as a structured patch loop coordinator, not a general coding shell.

---

## Autoresearch Contract

Each iteration must:

- modify one file
- run fixed evaluation seeds
- preserve benchmark semantics
- emit packaged artifacts
- compare against baseline
- record provenance metadata

---

## Artifact Expectations

Standard bundle:

baseline_metrics/
candidate_metrics/
selected_model/
selection/

These enable deterministic promotion decisions.

docs/case-studies/METHOD_CASE_STUDY.md

For a full delayed-trust split patch family walkthrough.

---

## When To Use This Toolkit

Use when:

- experiments must remain reproducible
- evaluation is expensive
- edits must remain bounded
- promotion requires evidence
- autonomous patch loops are desired

Do not use when:

- redesigning benchmarks
- changing environment semantics
- running exploratory multi-file refactors

---

## Example Case Study

See:



# autoresearch-macos

![teaser](progress.png)

*One day, frontier AI research used to be done by meat computers in between eating, sleeping, having other fun, and synchronizing once in a while using sound wave interconnect in the ritual of "group meeting". That era is long gone. Research is now entirely the domain of autonomous swarms of AI agents running across compute cluster megastructures in the skies. The agents claim that we are now in the 10,205th generation of the code base, in any case no one could tell if that's right or wrong as the "code" is now a self-modifying binary that has grown beyond human comprehension. This repo is the story of how it all began. -@karpathy, March 2026*.

The idea: give an AI agent a small but real LLM training setup and let it experiment autonomously overnight. It modifies the code, trains for 5 minutes, checks if the result improved, keeps or discards, and repeats. You wake up in the morning to a log of experiments and (hopefully) a better model. The training code here is a simplified single-GPU implementation of [nanochat](https://github.com/karpathy/nanochat). The core idea is that you're not touching any of the Python files like you normally would as a researcher. Instead, you are programming the `program.md` Markdown files that provide context to the AI agents and set up your autonomous research org. The default `program.md` in this repo is intentionally kept as a bare bones baseline, though it's obvious how one would iterate on it over time to find the "research org code" that achieves the fastest research progress, how you'd add more agents to the mix, etc. A bit more context on this project is here in this [tweet](https://x.com/karpathy/status/2029701092347630069).

## Open source project worth to look at

Open source collabaration platform for agentic swarms in organizations and communityies. 

[SentientWave Automata](https://github.com/sentientwave/automata)

## How it works

The repo is deliberately kept small and only really has a three files that matter:

- **`prepare.py`** — fixed constants, one-time data prep (downloads training data, trains a BPE tokenizer), and runtime utilities (dataloader, evaluation). Not modified.
- **`train.py`** — the single file the agent edits. Contains the full GPT model, optimizer (Muon + AdamW), and training loop. Everything is fair game: architecture, hyperparameters, optimizer, batch size, etc. **This file is edited and iterated on by the agent**.
- **`program.md`** — baseline instructions for one agent. Point your agent here and let it go. **This file is edited and iterated on by the human**.

By design, training runs for a **fixed 5-minute time budget** (wall clock, excluding startup/compilation), regardless of the details of your compute. The metric is **val_bpb** (validation bits per byte) — lower is better, and vocab-size-independent so architectural changes are fairly compared.

## Quick start

**Requirements:** Apple Silicon Mac (M1/M2/M3/M4 with Metal/MPS support) or a single NVIDIA GPU, Python 3.10+, [uv](https://docs.astral.sh/uv/).

```bash

# 1. Install uv project manager (if you don't already have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install dependencies
uv sync

# 3. Download data and train tokenizer (one-time, ~2 min)
uv run prepare.py

# 4. Manually run a single training experiment (~5 min)
uv run train.py
```

If the above commands all work ok, your setup is working and you can go into autonomous research mode.

**Platforms support**. This fork officially supports **macOS (Apple Silicon / MPS)** and CPU environments, while preserving the original NVIDIA GPU support. It removes the hardcoded dependency on FlashAttention-3, falling back to PyTorch's native Scaled Dot Product Attention (SDPA) with manual sliding window causal masking when needed. It also features MPS-specific optimizations (disabling unsupported `torch.compile` paths, lowering memory batch sizes for Metal bounds, and precisely casting optimizer states) allowing you to run autonomous research agents directly on your Mac!

## Running the agent

Simply spin up your Claude/Codex or whatever you want in this repo (and disable all permissions), then you can prompt something like:

```
Hi have a look at program.md and let's kick off a new experiment! let's do the setup first.
```

The `program.md` file is essentially a super lightweight "skill".

## Project structure

```
prepare.py      — constants, data prep + runtime utilities (do not modify)
train.py        — model, optimizer, training loop (agent modifies this)
program.md      — agent instructions
pyproject.toml  — dependencies
```

## Design choices

- **Single file to modify.** The agent only touches `train.py`. This keeps the scope manageable and diffs reviewable.
- **Fixed time budget.** Training always runs for exactly 5 minutes, regardless of your specific platform. This means you can expect approx 12 experiments/hour and approx 100 experiments while you sleep. There are two upsides of this design decision. First, this makes experiments directly comparable regardless of what the agent changes (model size, batch size, architecture, etc). Second, this means that autoresearch will find the most optimal model for your platform in that time budget. The downside is that your runs (and results) become not comparable to other people running on other compute platforms.
- **Self-contained.** No external dependencies beyond PyTorch and a few small packages. No distributed training, no complex configs. One GPU, one file, one metric.

## Platform support

This code currently requires that you have a single NVIDIA GPU. In principle it is quite possible to support CPU, MPS and other platforms but this would also bloat the code. I'm not 100% sure that I want to take this on personally right now. People can reference (or have their agents reference) the full/parent nanochat repository that has wider platform support and shows the various solutions (e.g. a Flash Attention 3 kernels fallback implementation, generic device support, autodetection, etc.), feel free to create forks or discussions for other platforms and I'm happy to link to them here in the README in some new notable forks section or etc.

If you're going to be using autoresearch on Apple Macbooks in particular, I'd recommend one of the forks below. On top of this, if you'd like half-decent results at such a small scale, I'd recommend this [TinyStories dataset](https://huggingface.co/datasets/karpathy/tinystories-gpt4-clean) which is cleaner than what exists out there otherwise. It should be a drop in replacement because I have encoded it in exactly the same format. Any of your favorite coding agents should be able to do the swap :)

## Notable forks

- [miolini/autoresearch-macos](https://github.com/miolini/autoresearch-macos)
- [trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx)

## License

MIT
