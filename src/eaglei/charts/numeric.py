"""Numbers — no art, just the ledger: free vs occupied vs running, aligned."""

from .. import theme


def _fmt(label: str, value: str, pct: float | None, width: int, pad: int) -> str:
    label_col = label[: max(pad - 2, 4)]
    val_col = value
    if pct is not None:
        c = theme.bar_color(pct)
        row = f"[dim #0f8038]{label_col:<{pad}}[/][{c}]{val_col}[/]"
    else:
        row = f"[dim #0f8038]{label_col:<{pad}}[/][bold #3dff7a]{val_col}[/]"
    return row


def render(data: dict, width: int, height: int) -> str:
    """`fields`: list of (label, value[, severity_pct]); None = blank spacer."""
    fields = data.get("fields") or [
        ("load", f"{data.get('percent', 0):.1f}%", data.get("percent")),
    ]
    fields = fields[: max(height, 1)]
    pad = max(len(f[0]) for f in fields if f is not None) + 2 if fields else 8
    rows = []
    for f in fields:
        if f is None:
            rows.append("")
            continue
        label, value = f[0], str(f[1])
        pct = f[2] if len(f) > 2 and f[2] is not None else None
        rows.append(_fmt(label, value, pct, width, pad))
    return "\n".join(rows)
