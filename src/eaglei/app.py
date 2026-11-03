"""EagleEye app assembly. The hawk takes wing."""

import random

from textual.app import App

from eaglei import charts

from .screens.detail import DetailScreen
from .screens.overview import Overview
from .screens.fetch import FetchScreen
from .screens.widgets import LABELS, Wing

CSS = """
Screen { background: #020803; }

HawkHeader {
    height: 1;
    padding: 0 1;
    color: #00ff41;
}

#wings {
    height: 1fr;
}

Wing {
    width: 1fr;
    height: 1fr;
    border: round #0f8038;
    margin: 0 1;
    padding: 0 1;
    color: #3dff7a;
    background: #020803;
}
Wing:focus {
    border: solid #00ff41;
    background: #04180a;
}

#dock {
    dock: bottom;
    height: 1;
    background: #030a04;
}

#detail-title { height: 1; padding: 0 1; }

#detail-gauges {
    width: 36;
    height: 100%;
    padding: 1 2;
    color: #3dff7a;
    border: round #0f8038;
    margin: 1;
}
#detail-right {
    width: 1fr;
    height: 100%;
    padding: 1;
}
#detail-table {
    height: 1fr;
    background: #020803;
}
#detail-table .datatable--cursor {
    background: #0f8038;
}
#detail-table .datatable--hover {
    background: #063014;
}
#detail-table > .datatable--header {
    color: #00ff41;
    text-style: bold;
}
#detail-footer {
    dock: bottom;
    height: 1;
    padding: 0 1;
}

.dock-label {
    height: 1;
    color: #0f8038;
    padding: 0 1;
    width: auto;
}
.chip {
    height: 1;
    color: #0f8038;
    padding: 0 1 0 0;
    width: auto;
}
.chip:hover {
    color: #99ffbb;
}
"""

BINDINGS = [
    ("q", "quit", "Quit"),
    ("tab", "focus_next", "Next wing"),
    ("shift+tab", "focus_previous", "Prev wing"),
    ("enter", "drill", "Drill into wing"),
    ("r", "shuffle", "Shuffle vizzes"),
    ("1", "viz(1)", ""),
    ("2", "viz(2)", ""),
    ("3", "viz(3)", ""),
    ("4", "viz(4)", ""),
    ("5", "viz(5)", ""),
    ("6", "viz(6)", ""),
    ("7", "viz(7)", ""),
]


class EagleEyeApp(App):
    TITLE = "EagleEye"
    CSS = CSS
    BINDINGS = BINDINGS

    def __init__(self) -> None:
        super().__init__()
        self.seed = random.randint(1, 999_999)  # session viz-seed, shown in header
        self.wing_kinds = ["cpu", "ram", "disk", "gpu"]
        self.wing_types: list[str] | None = None  # set on mount (needs Overview.CHARTS)

    def on_mount(self) -> None:
        # first shuffle of the session — the vizzes are random by design
        self.wing_types = charts.shuffle(len(self.wing_kinds), seed=self.seed)
        self.install_screen(Overview(), name="overview")
        self.install_screen(FetchScreen(), name="fetch")
        # boot into the fetch splash — eagle + hardware ledger first
        self.push_screen("fetch")

    # ---- helpers -----------------------------------------------------------
    def _focused_wing(self) -> Wing | None:
        foc = self.focused
        return foc if isinstance(foc, Wing) else None

    def _wings(self) -> list[Wing]:
        return list(self.query(Wing))

    # ---- viz actions -------------------------------------------------------
    def action_viz(self, n: int) -> None:
        """Nth chart type (dock order) onto the focused wing (or first wing)."""
        wing = self._focused_wing() or next(iter(self._wings()), None)
        if wing is None or not (1 <= n <= len(charts.ORDER)):
            return
        wing.chart_type = charts.ORDER[n - 1]
        wing.focus()
        wing.refresh()

    def action_shuffle(self) -> None:
        """Randomize chart type of every wing (fresh seed lineage)."""
        self.chart_seed = (getattr(self, "chart_seed", self.seed) * 31 + 17) % 1_000_003
        types = charts.shuffle(len(self.wing_kinds), seed=self.chart_seed)
        wings = self._wings()
        for wing, ctype in zip(wings, types * (len(wings) // len(types) + 1)):
            wing.chart_type = ctype
            wing.refresh()
        self.notify(f"[#00ff41]hawk re-focused · seed {self.chart_seed}[/#00ff41]")

    def action_drill(self) -> None:
        """Enter (or click) on focused wing → detail screen."""
        from .screens.widgets import LABELS

        wing = self._focused_wing()
        if wing is None:
            self.notify("[#ffd633]focus a wing first[#ffd633]")
            return
        self.push_screen(DetailScreen(wing.kind, LABELS[wing.kind]))
