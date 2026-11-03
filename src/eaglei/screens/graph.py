"""Graph screen — full-screen time-series dashboard. All metrics over time."""

import datetime
import os

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static

from .. import charts
from .. import theme
from ..sources import cpu as cpu_src
from ..sources import disk as disk_src
from ..sources import memory as mem_src
from ..sources import gpu as gpu_src


class GraphScreen(Screen):
    """Rolling history graph for CPU, RAM, GPU, Disk — press Esc to return."""

    BINDINGS = [("escape", "back", "Return to dashboard")]

    def __init__(self) -> None:
        super().__init__()
        self._hist: dict[str, list[float]] = {"cpu": [], "ram": [], "gpu": [], "disk": []}

    def compose(self) -> ComposeResult:
        yield Static(id="graph-title")
        with Horizontal(id="graph-rows"):
            with Vertical(id="graph-left"):
                yield Static(id="graph-cpu")
                yield Static(id="graph-ram")
            with Vertical(id="graph-right"):
                yield Static(id="graph-gpu")
                yield Static(id="graph-disk")

    def on_mount(self) -> None:
        self.set_interval(1.0, self._refresh)
        self._refresh()

    def _refresh(self) -> None:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        host = os.uname().nodename
        self.query_one("#graph-title").update(
            f"[bold {theme.FG}]═ GRAPH — {host} @ {now}[/]  [dim {theme.DIM}]Esc = dashboard[/]"
        )

        pairs = (
            ("graph-cpu", "CPU", cpu_src.collect, "cpu"),
            ("graph-ram", "RAM", mem_src.collect, "ram"),
            ("graph-gpu", "GPU", gpu_src.collect, "gpu"),
            ("graph-disk", "DISK", disk_src.collect, "disk"),
        )
        for wid, label, collect_fn, key in pairs:
            d = collect_fn()
            pct = d.get("percent", 0.0)
            self._hist[key].append(pct)
            if len(self._hist[key]) > 60:
                self._hist[key] = self._hist[key][-60:]
            self.query_one(f"#{wid}", Static).update(
                charts.CHARTS["graph"](
                    {"label": label, "percent": pct, "history": list(self._hist[key])},
                    56,
                    16,
                )
            )

    def action_back(self) -> None:
        self.app.pop_screen()
