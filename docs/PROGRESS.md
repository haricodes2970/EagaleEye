# EagleEye (EGLEI) — Project Context

This file preserves the full state of the project so a new chat can pick up exactly where we left off.

## What EagleEye is

A neon-green, hacker-styled terminal dashboard + task manager for Linux.
Type **`eye`** in any terminal → opens the dashboard. Never leaves the terminal.
Shows live data visualizations for CPU, RAM, Disks, GPU with Task-Manager-style
drill-downs into per-process resource usage. Built in Python with Textual.

## Current version

**v0.1.5** — tag `v0.1.5` pushed to `main`.

Repo: `https://github.com/haricodes2970/EagaleEye`
Local: `/home/hari007/Projects/Personal/EagaleEye` (folder renamed from `EagalEye`)
Git remote: `origin` → `https://github.com/haricodes2970/EagaleEye.git`
Branch: `main`

## Installation

**Auto-install latest (recommended):**
```bash
curl -fsSL https://github.com/haricodes2970/EagaleEye/raw/main/install.sh | sh
eye
```
`install.sh` uninstalls + reinstalls from `main` every run → always latest.

**From repo:**
```bash
git clone https://github.com/haricodes2970/EagaleEye.git
cd EagaleEye
python3 -m venv .venv && . .venv/bin/activate
pip install -e .[dev]
pytest && eye
```

**Command:** `eye` (also supports `eye --version`)

## Screen flow (verified end-to-end in real terminal pty)

```
eye
  └─ fetch screen (boot splash)
       ├─ any key / click / Enter / Space → dashboard
       └─ q → quit
  dashboard (Overview)
       ├─ ↑↓←→ / click → focus a wing (CPU / RAM / DISK / GPU)
       ├─ 1..0 → change focused wing's viz type (bar / numbers / pie / sparkline /
       │       gauge / radial / graph / area / scatter / heatmap / histogram)
       ├─ R → shuffle-randomize all wing vizzes
       ├─ Enter / click wing → drill-down (Task-Manager detail screen)
       ├─ g → full-screen time-series graph screen
       ├─ Esc → back to fetch screen
       └─ q → quit
  detail screen
       └─ Esc → back to dashboard
  graph screen
       └─ Esc → back to dashboard
```

## Theme

**Neon-green hacker / cybersell:** phosphor `#00ff41` on near-black `#020803`.
Severity colors: green <75%, yellow 75–90%, red >90%. All charts share one
severity ramp. ASCII hawk glyph `◖◉▬◉◗` + full block-glyph eagle art on the fetch
screen.

## Code layout

```
EagaleEye/
├── pyproject.toml          # name=eagaleeye, entrypoint eye = eaglei.cli:main
├── install.sh              # auto-install-latest from GitHub main
├── README.md
├── src/eaglei/
│   ├── __init__.py         # __version__ = "0.1.5"
│   ├── cli.py              # `eye` entrypoint, --version flag
│   ├── app.py              # EagleEyeApp(Textual App), screen wiring
│   ├── theme.py            # FG, MID, DIM, BG, ALERT, WARN, RAMP, STYLES
│   ├── logo.py             # hawk emblem + tagline
│   ├── art/
│   │   ├── __init__.py
│   │   └── eagle.py        # block-glyph eagle art + neon ramp stripes
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── fetch.py        # Boot screen: eagle art + hardware/session/uptime ledger
│   │   ├── overview.py     # Dashboard: 4 wings grid + dock bar (viz chips)
│   │   ├── detail.py       # Drill-down: per-core CPU, RAM procs, GPU VRAM procs, disks
│   │   ├── graph.py        # Time-series graph screen (CPU/RAM/GPU/Disk history)
│   │   └── widgets.py      # Wing widget (poller + swappable chart renderer)
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── cpu.py          # psutil cpu: percent, per_core, freq, load_avg, model, top procs
│   │   ├── memory.py       # psutil mem: RAM/swap, top procs by RSS
│   │   ├── disk.py         # LUKS-aware partitions, read/write MB/s rates
│   │   └── gpu.py          # nvidia-smi: VRAM%, util%, per-process VRAM (cached)
│   └── charts/
│       ├── __init__.py     # CHARTS registry + ORDER (11 types) + shuffle()
│       ├── bar.py          # horizontal percent bar
│       ├── numbers.py      # plain ledger: free/occupied/running counts
│       ├── pie.py          # ASCII donut sweep
│       ├── sparkline.py    # unicode block history
│       ├── gauge.py        # severity bracket bar
│       ├── radial.py       # semicircular dial
│       ├── graph.py        # ASCII line plot
│       ├── area.py         # filled area chart
│       ├── scatter.py      # per-core/per-process dots
│       ├── heatmap.py      # dot matrix grid
│       └── histogram.py    # distribution bars
└── tests/
    ├── test_cpu_memory.py  # 4 tests
    ├── test_disk_gpu.py    # 3 tests
    ├── test_charts.py      # markup-safe render tests
    └── test_numbers.py     # numbers viz tests
```
44 tests pass (`pytest`).

## Key implementation notes

- **Sources are hardware-facing only** — they return plain dicts; screens/charts never import psutil directly.
- **Charts are dumb** — `render(data, width, height) -> str`, duck-typed contract, markup-safe via Rich.
- **Wing widget** polls its source on an interval, keeps a rolling history, switches chart type via `chart_type`.
- **Fetch screen boots first** — eagle art on left, CPU/GPU/RAM/SWAP/DRIVE bars + LOGIN/UPTIME/DATE + palette dots on right.
- **GPU** uses `nvidia-smi`; degrades silently to `available: false` on non-NVIDIA.
- **Disk** skips squashfs/tmpfs/devtmpfs; computes per-device IO rates from deltas.
- **Textual Screen base classes** for fetch/overview/graph/detail (pop/push screen stack).
- **pipx** is the distribution vehicle (`pipx install git+...` or `install.sh`).

## Commits on main (latest first)

- `0e89d9f` feat(graphify): area, scatter, heatmap, histogram + GraphScreen (g key); 44 tests
- `494ee8f` chore: version 0.1.3, eye --version support
- `432ab22` docs: README keys table + fetch boot screen flow
- `269570d` feat(art): neon-green block-glyph eagle hawk mascot art
- `82221e4` feat: wing-click drill-downs, dock-chip viz switching, GPU process name cleanup, install.sh + README
- `354ecbe` feat(charts): six-visualization kit + registry + shuffle; 25 tests
- `b1f35ef` feat(sources): disk + gpu sources; 7 tests
- `33f4d0f` feat(sources): cpu + memory collectors; editable install verified
- `caa5c58` feat(theme): NEON GREEN hacker palette + eagle emblem
- `e4b94c0` chore: project skeleton

## Tags

`v0.1.0` `v0.1.1` `v0.1.2` `v0.1.3` `v0.1.4` `v0.1.5` — all pushed to origin.

## Suggested next work (batch b)

1. **PyPI publish** → `pipx install eagaleeye` shortest path
2. **Extra metric wings:** network up/down per interface, NVML temps, battery health
3. **Persist favorite viz per wing** (config file + session-seed flag)
4. **Snapshot screenshots into README**
5. **CI** (GitHub Actions: pytest on push)

## Environment used to build/test

- Fedora Linux, Python 3.14.8, pip 26.0.1
- textual 8.2.8, psutil 7.2.2
- Hardware probed live: AMD Ryzen 7 7435HS ×16 cores, 16 GB RAM + 8 GB zram,
  477 GB LUKS NVMe, NVIDIA GeForce RTX 3050 Laptop 4 GB VRAM

## Known limitations

- GPU wing is NVIDIA-only via `nvidia-smi`; other GPUs show "not detected"
- `install.sh` uses pipx; machines without pipx get bootstrapped
- No image logo yet — ASCII hawk only; drop a PNG in `assets/` to replace
