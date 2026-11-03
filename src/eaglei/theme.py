"""NEON GREEN HACKER theme — phosphor-green on near-black, hawk-grade contrast."""

# Core palette (hex, no alpha — terminal safe)
FG = "#00ff41"  # phosphor neon green
MID = "#3dff7a"  # brighter accent green
DIM = "#0f8038"  # dim structural green
BG = "#020803"  # near-black green tint
ALERT = "#ff3341"  # cpu > 90%
WARN = "#ffd633"  # cpu > 75%

# Chart accent ramp (used by pie/radial/segments, stays in-family)
RAMP = ["#00ff41", "#2bff60", "#26e85c", "#1fb84a", "#168f3a", "#0f6b2b", "#0a4a1e", "#063014"]


def bar_color(percent: float) -> str:
    """Pick foreground color by how hot a metric is."""
    if percent >= 90:
        return ALERT
    if percent >= 75:
        return WARN
    return FG


# Semantic style map (drag into any widget: styles["title"] etc.)
STYLES = {
    "title": f"bold {FG}",
    "subtitle": f"italic {DIM}",
    "border": DIM,
    "border_focus": f"bold {FG}",
    "header": f"bold {FG} on {BG}",
    "footer_key": f"bold {FG}",
    "footer_dim": DIM,
    "ok": FG,
    "warn": WARN,
    "alert": ALERT,
}


def markup(value: float, text: str) -> str:
    """Markup a string in the severity color of `value` (0-100)."""
    return f"[{bar_color(value)}]{text}[/{bar_color(value)}]"
