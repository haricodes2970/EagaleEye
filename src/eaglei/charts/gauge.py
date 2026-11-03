"""Gauge — big severity-colored readout + bracket bar."""

from .. import theme
from ..theme import bar_color


def render(data: dict, width: int, height: int) -> str:
    percent = max(0.0, min(100.0, float(data.get("percent", 0))))
    label = data.get("label", "load")
    c = bar_color(percent)
    # huge numeral row in the middle of the card
    big = f"[7;5;8bold] " if False else ""
    bar_w = max(4, width - 14)
    filled = round(percent / 100 * bar_w)
    bar = f"[{c}]{'━' * filled}[/][{theme.DIM}]{'╌' * (bar_w - filled)}[/{theme.DIM}]"
    caption = data.get("caption", "")
    lines = []
    pad_top = max(height - 4, 1) // 2
    lines += [""] * pad_top
    lines.append(f"[bold {c}]{percent:6.1f}%[/]".center(width))
    lines.append(f"{label} {bar} {caption}")
    return "\n".join(lines)
