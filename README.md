# 🦅 EagleEye (EGLEI)

> You open your terminal. You type **`eye`**. The hawk watches over your system.

A neon-green, hacker-styled terminal dashboard + task manager for Linux —
data visualizations for CPU, RAM, Disks and GPU that never look the same
twice, with Task-Manager-style drill-downs for every resource.

```
┌ CPU ──────────┐ ┌ RAM ───────┐ ┌ GPU ──────┐ ┌ DISK ─────┐
│ 16-core radar │ │ bar grid   │ │ VRAM gauge│ │ hbar stack│
└───────────────┘ └────────────┘ └───────────┘ └───────────┘
 bar | pie | sparkline | gauge | radial | graph     ← swap any wing live
```

## Install

```bash
# simplest — bootstrap straight from this repo (npm -g equivalent)
curl -fsSL https://github.com/haricodes2970/EagaleEye/raw/main/install.sh | sh

# or, if you already use pipx
pipx install git+https://github.com/haricodes2970/EagaleEye.git

# then, in any terminal:
eye
```

Requirements: Linux, Python 3.10+, a terminal that supports mouse events.
GPU wing is NVIDIA-friendly (`nvidia-smi`) and degrades silently on other GPUs.

## Keys

| Key | Action |
|---|---|
| `↑↓←→` / click | focus a wing |
| `1..0` | change the focused wing's visualization (bar, numbers, pie, sparkline, gauge, radial, graph, area, scatter, heatmap, histogram) |
| `R` | shuffle — randomize every wing's visualization |
| `Enter` / click wing | drill down (Task-Manager detail screen) |
| `g` | full-screen time-series graph of all metrics |
| `Esc` | detail → dashboard → fetch screen |
| `q` | quit |

On boot `eye` opens the **fetch screen**: a neon-green block-glyph hawk left; hardware/session/uptime ledger right — same structured look as your references, eagle instead of lotus/spider. Any key opens the live dashboard.

## Graph screen

Press `g` on the dashboard for a rolling time-series graph of CPU, RAM, GPU and Disk usage over the last 60 samples. Esc returns to the dashboard.


## Build yours

```bash
git clone https://github.com/haricodes2970/EagaleEye.git
cd EagaleEye
python3 -m venv .venv && . .venv/bin/activate
pip install -e .[dev]
pytest && eye
```

## Branding

The built-in emblem is ASCII (see `src/eaglei/logo.py`) — neon-green hawk's eye.
An official image logo can live in `assets/` once designed; the tattoo is optional.

## License

MIT
