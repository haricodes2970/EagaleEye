"""Scatter plot — per-core / per-process resource dots, severity-colored."""

from ..theme import bar_color


def render(data: dict, width: int, height: int) -> str:
    """`points`: list of (x, y, pct, label).  Falls back to a synthetic core fan-out."""
    points = data.get("points")
    label = data.get("label", "cores")
    if not points:
        cores = data.get("per_core", [float(data.get("percent", 0))])[: max(width // 4, 1)]
        points = [(i * 4 + 2, v, v, f"c{i}") for i, v in enumerate(cores)]

    grid: list[list[str]] = [[" "] * width for _ in range(max(height - 1, 2))]
    for x, y, pct, _name in points:
        px = min(width - 1, max(0, int(x)))
        py = min(len(grid) - 1, max(0, int(y / 100 * (len(grid) - 1))))
        c = bar_color(pct)
        grid[len(grid) - 1 - py][px] = f"[{c}]●[/]"

    lines = ["".join(r) for r in grid]
    mx = max((p[1] for p in points), default=0.0)
    lines.append(f"{label} scatter [bold]{mx:5.1f}%[/] peak")
    return "\n".join(lines[:height])
