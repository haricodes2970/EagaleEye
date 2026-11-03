"""Bar — horizontal percent bar with gradient blocks and end label."""

from .. import theme
from ..theme import bar_color

BLOCKS = "         "  # (reserved for sub-block resolution)


def render(data: dict, width: int, height: int) -> str:
    """Multibar card: one row per value in data['rows'], plus summary row.

    Rows present (label, percent, caption). Fallback to single 'percent'.
    """
    rows = data.get("rows") or [(data.get("label", "load"), float(data.get("percent", 0)), "")]
    lines = []
    for label, pct, caption in rows:
        pct = max(0.0, min(100.0, pct))
        frac = pct / 100.0
        dim_cells = round(frac * width * 0.55)
        hot_cells = round(frac * width) - dim_cells
        hot_cells = max(0, hot_cells)
        empty = max(0, width - round(frac * width))
        c = bar_color(pct)
        bar = f"[{theme.DIM}]{'▓' * dim_cells}[/{theme.DIM}][{c}]{'█' * hot_cells}[/{c}][{theme.BG}]{'·' * empty}[/{theme.BG}]"
        lines.append(f"{label:<8} {bar} [bold {c}]{pct:5.1f}%[/]  {caption}")
    return "\n".join(lines[: max(height - 1, 1)])
