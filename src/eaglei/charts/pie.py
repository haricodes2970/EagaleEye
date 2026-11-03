"""Pie — ASCII donut: used slice in neon ramp, remaining in dim."""

import math

from .. import theme
from ..theme import bar_color


def render(data: dict, width: int, height: int) -> str:
    percent = float(data.get("percent", 0))
    label = data.get("label", "load")
    rx = max(6, width // 2 - 4)
    ry = max(3, height - 2)
    rows = []
    for y in range(ry * 2):
        # ellipse ring: keep only edge cells for donut look
        line = ""
        for x in range(rx * 2):
            dx = (x - rx + 0.5) / rx
            dy = (y - ry + 0.5) / ry
            d = math.hypot(dx, dy)
            if 0.75 <= d <= 1.05:
                angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360
                # mark slice starting at top (-90°), clockwise
                slice_start = -90
                idx = (angle - slice_start) % 360
                frac = idx / 360.0
                line += (
                    f"[{bar_color(percent)}]█[/{bar_color(percent)}]"
                    if frac <= percent / 100.0
                    else f"[{theme.DIM}]░[/{theme.DIM}]"
                )
            else:
                line += " "
        rows.append(line)
    pct_txt = f"[bold {bar_color(percent)}]{percent:5.1f}%[/]"
    legend = f"{label} used {pct_txt}"
    return "\n".join(rows[: max(height - 1, 1)]) + "\n" + legend
