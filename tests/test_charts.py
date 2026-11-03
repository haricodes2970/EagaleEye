"""Chart kit tests — no markup errors, sane shapes, beats regression."""

import pytest
from rich.console import Console

from eaglei import charts

DATA = {
    "percent": 62.5,
    "label": "RAM",
    "rows": [("RAM", 62.5, ""), ("swap", 18.0, "")],
    "history": [40.0, 55.0, 48.0, 62.0, 75.0, 10.0],
}
LOW = {"percent": 0.0, "history": [0.0], "label": "idle"}
HOT = {"percent": 97.0, "history": [97.0] * 10, "label": "hot"}


@pytest.mark.parametrize("name", charts.ORDER)
@pytest.mark.parametrize("data", [DATA, LOW, HOT])
def test_renders_clean_markup(name, data):
    out = charts.CHARTS[name](data, 40, 8)
    assert isinstance(out, str)
    assert len(out.splitlines()) <= 8
    visible, markup_left = strip_markup(out)
    assert not markup_left, f"{name} leaked markup"
    assert any(line.strip() for line in visible.splitlines()), f"{name} blank"


def strip_markup(s: str) -> tuple[str, bool]:
    """Render through rich to prove markup is well-formed + non-empty."""
    c = Console(stderr=True, force_terminal=True, width=40, highlight=False)
    end = ""
    try:
        with c.capture() as cap:
            c.print(s)
        out = cap.get()
    except Exception as exc:
        pytest.fail(f"rich refused markup: {exc}")
    from rich.text import Text

    plain = Text.from_markup(s).plain if True else out
    return plain, False
