"""Sparkline — unicode intensity blocks over a rolling history."""

from ..theme import bar_color


def render(data: dict, width: int, height: int) -> str:
    percent = float(data.get("percent", 0))
    history = data.get("history") or [percent]
    label = data.get("label", "load")
    blocks = "▁▂▃▄▅▆▇█"
    hist = [max(0.0, min(100.0, h)) for h in history][-width:]
    glyphs = "".join(blocks[int(h / 100 * (len(blocks) - 1))] for h in hist)
    c = bar_color(max(hist or [0]))
    lines = [""] * max(height - 3, 0)
    lines.append(f"[bold {c}]{glyphs}[/]")
    peak = max(hist or [0.0])
    lines.append(f"{label} peak {peak:5.1f}%")
    return "\n".join(lines)
