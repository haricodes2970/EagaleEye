"""Overview screen: hawk eye header, four wings, and the chart dock."""

from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static

from .. import charts
from ..logo import LOGO, TAGLINE
from ..sources.cpu import collect as cpu_collect
from ..sources.memory import collect as mem_collect
from .widgets import Wing

ORDER = charts.ORDER  # viz types, dock order


class HawkHeader(Static):
    """Emblem + host vitals line, phosphor green."""

    def on_mount(self) -> None:
        self.set_interval(2.0, self.refresh_now)
        self.refresh_now()

    def refresh_now(self) -> None:
        import platform
        import time

        secs = time.time() - psutil_boot()
        host = platform.node()
        cpu = cpu_collect()
        ram = mem_collect()

        line = (
            f"[bold #00ff41]◉ EAGLE EYE[/bold #00ff41][dim #0f8038]│ {host} │ "
            f"up {int(secs // 3600)}h{int(secs % 3600 // 60):02d}m │ "
            f"CPU {cpu['percent']:4.1f}% │ [bold #3dff7a]{cpu['cores']}c[/] │ "
            f"RAM {ram['percent']:4.1f}%[/]"
        )
        self.update(line)


def psutil_boot() -> float:
    import psutil

    return psutil.boot_time()


class DockChip(Static):
    """Clickable viz-type chip in the dock."""

    can_focus = False

    def __init__(self, viz: str, index: int) -> None:
        super().__init__(f"{index}: {viz}", classes="chip", id=f"chip-{viz}")
        self.viz = viz

    def on_click(self) -> None:
        from .widgets import Wing

        app = self.app
        wing = app._focused_wing() or next(iter(app.screen.query(Wing)), None)
        if wing is None:
            return
        wing.chart_type = self.viz
        wing.focus()
        wing.refresh()


class Overview(Screen):
    """Default screen — wings grid + dock."""

    BINDINGS = [
        ("1,2,3,4,5,6", "viz", "switch viz of focused wing"),
        ("r", "shuffle", "shuffle all wing vizzes"),
        ("enter", "drill", "drill into focused wing"),
    ]

    def compose(self) -> ComposeResult:
        seed = getattr(self.app, "seed", 0)
        yield HawkHeader(TAGLINE + f"  ·  seed {seed}")
        wings = getattr(self.app, "wing_kinds", ["cpu", "ram", "disk", "gpu"])
        types = getattr(self.app, "wing_types", ["bar"] * len(wings))
        with Horizontal(id="wings"):
            for kind, ctype in zip(wings, types):
                yield Wing(kind, ctype)
        with Horizontal(id="dock"):
            yield Static("[dim #0f8038]viz ▸[/]", classes="dock-label")
            for i, name in enumerate(ORDER, 1):
                yield DockChip(name, i)


def wing_types_for(count: int, seed: int) -> list[str]:
    import random

    return charts.shuffle(count, seed=seed)
