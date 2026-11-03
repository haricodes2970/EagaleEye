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
# from this repository directly (npm -g equivalent for Python)
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
| `1..6` | change the focused wing's visualization (pie, bar, gauge, …) |
| `R` | shuffle — randomize every wing's visualization |
| `Enter` / click wing | drill down (Task-Manager detail screen) |
| `Esc` | back to overview |
| `q` | quit |

## Build yours

```bash
git clone https://github.com/haricodes2970/EagaleEye.git
cd EagaleEye
python3 -m venv .venv && . .venv/bin/activate
pip install -e .[dev]
pytest && eye
```

## License

MIT
