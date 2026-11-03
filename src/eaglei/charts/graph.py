"""Graph — ASCII line plot over rolling history with a severity-colored trace."""

from ..theme import bar_color


def render(data: dict, width: int, height: int) -> str:
    percent = float(data.get("percent", 0))
    label = data.get("label", "load")
    plot_rows = max(height - 2, 2)
    hist = [max(0.0, min(100.0, h)) for h in (data.get("history") or [percent])][-width:]
    hist += [hist[-1] if hist else 0.0] * (width - len(hist))  # pad left

    rows = [[" "] * width for _ in range(plot_rows)]
    lastx = lasty = None
    for x, v in enumerate(hist):
        y = plot_rows - 1 - round(v / 100 * (plot_rows - 1))
        rows[y][x] = "●"
        if lasty is not None:  # crude vertical join for continuity
            y0, y1 = (min(lasty, y), max(lasty, y))
            for yy in range(y0, y1):
                rows[yy][x] = "│"
        lastx, lasty = x, y

    c = bar_color(max(hist or [0.0]))
    lines = ["".join(r) for r in rows]
    lines.append(f"{label} line [bold {c}]{hist[-1]:5.1f}%[/]")
    return "\n".join(lines[:height])
