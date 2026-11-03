"""Pie — ASCII donut: used arc in severity color, rest dim. 2:1 terminal cells."""

import math

from .. import theme
from ..theme import bar_color


def render(data: dict, width: int, height: int) -> str:
    percent = max(0.0, min(100.0, float(data.get("percent", 0))))
    label = data.get("label", "load")
    c = bar_color(percent)
    rows_n = max(height - 1, 2)
    cols = max(10, width)

    # ellipse radii in cell space; cells are ~2x tall => dy spans twice dx per cell
    rx = (cols / 2) - 1.5
    ry = rows_n / 2.0

    out = []
    for j in range(rows_n):
        line = ""
        for i in range(cols):
            dx = (i + 0.5) - (cols / 2)
            dy = ((j + 0.5) - rows_n / 2.0) * 2.2  # aspect correction
            r = math.hypot(dx / max(1e-9, rx), dy / max(1e-9, ry))
            if 0.82 <= r <= 1.06:
                # clock angle: 0° at 12 o'clock, clockwise
                theta = (math.degrees(math.atan2(dx, -dy)) + 360) % 360
                filled = theta <= percent / 100.0 * 360.0
                line += f"[{c}]●[/{c}]" if filled else f"[{theme.DIM}]○[/{theme.DIM}]"
            elif r < 0.82:
                line += " "
            else:
                line += " "
        out.append(line)
    out.append(f"{label} used [bold {c}]{percent:5.1f}%[/]")
    return "\n".join(out[:height])
