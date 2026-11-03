"""Radial — ASCII dial: semicircular sweep from left, severity-colored, needle at fill edge."""

import math

from .. import theme
from ..theme import bar_color


def render(data: dict, width: int, height: int) -> str:
    percent = max(0.0, min(100.0, float(data.get("percent", 0))))
    label = data.get("label", "load")
    c = bar_color(percent)
    frac = percent / 100.0

    rows: list[str] = []
    dial_rows = max(height - 2, 2)  # top: dial, middle: baseline, bottom: legend
    W = max(10, width)
    grid = [[" "] * W for _ in range(dial_rows)]

    needle_col = int(frac * (W - 1))
    for x in range(W):
        theta = math.pi * (1 - x / (W - 1))  # left(π) → right(0)
        y = round((1 - math.sin(theta)) * (dial_rows - 1))
        if 0 <= y < dial_rows:
            grid[y][x] = "◈" if x == needle_col else ("█" if x <= needle_col else "░")

    rows = ["".join(r) for r in grid]
    rows.append("┕" + "─" * (W - 2) + "┙")
    rows.append(f"{label} dial [bold {c}]{percent:5.1f}%[/]")
    return "\n".join(rows[:height])
