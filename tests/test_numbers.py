"""Numbers-viz (ledger) tests — the plain-reading wing."""

from eaglei import charts

FIELDS = [
    ("occupied", "8.9G / 15.4G", 57.4),
    ("free", "6.5G", 42.6),
    ("swap used", "6.0G / 8.0G", 75.0),
    ("procs alive", "412"),
]


def test_numbers_renders_all_fields():
    out = charts.CHARTS["numbers"]({"label": "RAM", "fields": FIELDS}, 40, 10)
    lines = out.splitlines()
    assert len(lines) == len(FIELDS)
    flat = out
    assert "occupied" in flat and "8.9G" in flat
    assert "free" in flat and "6.5G" in flat
    assert "procs alive" in flat and "412" in flat


def test_numbers_truncates_to_height():
    out = charts.CHARTS["numbers"]({"label": "RAM", "fields": FIELDS}, 40, 3)
    assert len(out.splitlines()) <= 3


def test_numbers_falls_back_to_percent():
    out = charts.CHARTS["numbers"]({"percent": 42.0}, 30, 4)
    assert "42.0%" in out


def test_seven_viz_types_registered():
    assert len(charts.ORDER) == 11
    assert "numbers" in charts.ORDER
