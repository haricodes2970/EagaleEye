"""Heatmap — grid of resource dots (CPU cores, disk partitions, GPU procs)."""

from ..theme import bar_color


def render(data: dict, width: int, height: int) -> str:
    """`cells`: list of (label, pct); renders a severity-colored dot matrix."""
    cells = data.get("cells") or [
        ("load", float(data.get("percent", 0))),
    ]
    cols = max(4, min(width // 6, len(cells)))
    rows_n = max(height - 1, 2)
    cw = max(6, width // cols)
    glyphs = "·░▒▓█"

    lines: list[str] = []
    for r in range(rows_n):
        line = ""
        for c in range(cols):
            idx = r * cols + c
            if idx >= len(cells):
                line += " " * cw
                continue
            lbl, pct = cells[idx]
            frac = max(0.0, min(1.0, pct / 100.0))
            g = glyphs[min(len(glyphs) - 1, int(frac * (len(glyphs) - 1)))]
            cc = bar_color(pct)
            line += f"[{cc}]{g}[/{cc}]{lbl[: cw - 1]:<{cw - 1}}"
        lines.append(line[:width])
    lines.append(f"{data.get('label', 'heat')} heatmap")
    return "\n".join(lines[:height])
