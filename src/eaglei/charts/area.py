"""Area chart — filled line graph, severity gradient."""

from ..theme import bar_color


def render(data: dict, width: int, height: int) -> str:
    percent = float(data.get("percent", 0))
    label = data.get("label", "load")
    hist = [max(0.0, min(100.0, h)) for h in (data.get("history") or [percent])][-width:]
    hist += [hist[-1] if hist else 0.0] * (width - len(hist))

    plot_rows = max(height - 2, 2)
    c = bar_color(max(hist or [0.0]))
    rows: list[str] = []
    for y in range(plot_rows):
        line = ""
        level = y / max(plot_rows - 1, 1)
        for x, v in enumerate(hist):
            top = v / 100.0
            fill = level <= top
            if fill:
                edge = abs(level - top) < 0.08
                line += f"[{c}]{'▬' if edge else '█'}[/]"
            else:
                line += " "
        rows.append(line)
    rows.append(f"{label} area [bold {c}]{hist[-1]:5.1f}%[/]")
    return "\n".join(rows[:height])
