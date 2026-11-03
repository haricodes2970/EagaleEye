"""Histogram — distribution bar of value buckets."""

from ..theme import bar_color


def render(data: dict, width: int, height: int) -> str:
    """`buckets`: list of (label, count, pct). Falls back to single bar."""
    buckets = data.get("buckets") or [(data.get("label", "load"), float(data.get("percent", 0)), 100.0)]
    cols = max(1, width // 7)
    peak = max((b[2] for b in buckets), default=0.0)
    c = bar_color(peak)

    lines: list[str] = []
    plot_h = max(height - 2, 2)
    for y in range(plot_h):
        level = y / max(plot_h - 1, 1)
        line = ""
        for label, _count, pct in buckets:
            frac = pct / 100.0
            filled = level <= frac
            cell_w = cols
            if filled:
                edge = abs(level - frac) < 0.12
                line += f"[{c}]{'▬' if edge else '█'}[/]" + " " * max(cell_w - 1, 0)
            else:
                line += " " * cell_w
        lines.append(line[:width])
    lines.append(f"{buckets[0][0]} hist peak {peak:5.1f}%")
    return "\n".join(lines[:height])
