"""Detail drill-down screens — the Task Manager side of the hawk."""

from collections import deque

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import DataTable, Static

from .. import theme
from ..sources import cpu as cpu_src
from ..sources import disk as disk_src
from ..sources import gpu as gpu_src
from ..sources import memory as mem_src


class CoreBars(Static):
    """Per-core vertical bars for the CPU drill-down."""

    history: list[float]

    def render(self) -> str:
        d = cpu_src.collect()
        rows = []
        per_core = d["per_core"]
        cols = max(1, (self.size.width - 2) // 4)
        for chunk_start in range(0, len(per_core), cols):
            group = per_core[chunk_start : chunk_start + cols]
            lines = [[] for _ in range(5)]  # 5-cell tall bars
            for i, v in enumerate(group):
                c = theme.bar_color(v)
                filled = round(v / 100 * 5)
                for cell in range(5):
                    mark = "█" if cell < filled else "·"
                    lines[cell].append(f"[{c}]{mark}[/{c}]")
            head = " ".join(f"[dim #0f8038]c{chunk_start + i:<2}[/]" for i in range(len(group)))
            rows.append(head)
            rows += [" ".join(cells) for cells in lines]
        return "\n".join(rows) or "[dim]warming cores…[/]"


class DetailScreen(Screen):
    """Full-screen drill-down: live summary + top processes. Esc pops back."""

    BINDINGS = [("escape", "back", "back")]

    W = 18  # gauge column width

    def __init__(self, kind: str, label: str) -> None:
        super().__init__(id=f"detail-{kind}")
        self.kind = kind
        self.label = label

    def compose(self) -> ComposeResult:
        yield Static(f"[bold #00ff41]▚ {self.label}[/bold #00ff41]  [dim #0f8038]Esc to hunt elsewhere[/]", id="detail-title")
        with Horizontal():
            yield Static(id="detail-gauges")
            yield Vertical(id="detail-right")
        yield Static("", id="detail-footer")

    def on_mount(self) -> None:
        right = self.query_one("#detail-right")
        right.mount(DataTable(id="detail-table", cursor_type="row"))
        self._table().add_columns(*self._columns())
        self.set_interval(1.0, self._refresh)
        self._refresh()
        self._table().focus()

    # ---- per-kind table spec ------------------------------------------------
    def _columns(self) -> list[str]:
        unit = {"cpu": "CPU%", "ram": "MEM(GB)", "disk": "", "gpu": "VRAM(GB)"}[self.kind]
        base = ["PID", "NAME"]
        if self.kind == "disk":
            return ["MOUNT", "DEVICE", "USED", "TOTAL", "%",]
        return base + [unit]

    def _rows(self) -> list[tuple]:
        if self.kind == "cpu":
            return [(str(r["pid"]), r["name"], f"{r['value']:.1f}") for r in cpu_src.top_processes(20)]
        if self.kind == "ram":
            return [(str(r["pid"]), r["name"], f"{r['value']:.2f}") for r in mem_src.top_processes(20)]
        if self.kind == "gpu":
            return [
                (str(r["pid"]), r["name"], f"{r['value']:.2f}")
                for r in (gpu_src.top_processes(20) or [dict(pid=0, name="no VRAM holders", value=0)])
            ]
        d = disk_src.collect()
        return [
            (p["mountpoint"], p["device"], f"{p['used_gb']:.0f}G", f"{p['total_gb']:.0f}G", f"{p['percent']:.0f}%")
            for p in d["partitions"]
        ]

    def _gauge_text(self) -> str:
        """Left pane summary, per-kind."""
        w = self.W
        if self.kind == "cpu":
            d = cpu_src.collect()
            bars = _mini_bars(d["per_core"][:8], w)
            return f"[bold #00ff41]{d['cores']} cores[/]\n[{theme.FG}]{bars}[/]\n\nfreq [bold]{d['freq_mhz']:.0f}[/] MHz\nload {d['load_avg']}"
        if self.kind == "ram":
            d = mem_src.collect()
            frac = "█" * int(d["percent"] / 100 * w)
            return (
                f"RAM [bold]{d['used_gb']:.1f}G[/] / {d['total_gb']:.1f}G  {d['percent']:.1f}%\n"
                f"[{theme.bar_color(d['percent'])}]{frac:─<{w}}[/]\n\n"
                f"swap [bold]{d['swap_used_gb']:.1f}G[/] / {d['swap_total_gb']:.1f}G ({d['swap_percent']:.0f}%)\n"
                f"free in cache {d['available_gb']:.1f}G"
            )
        if self.kind == "gpu":
            d = gpu_src.collect()
            if not d.get("available"):
                return "[dim #0f8038]no NVIDIA GPU — hawk sees darkness[/]"
            frac = "█" * int(d["percent"] / 100 * w)
            return (
                f"[bold #00ff41]{d['device']}[/]\n"
                f"VRAM [bold]{d['used_mb']:.0f}[/] / {d['total_mb']:.0f} MB  {d['percent']:.1f}%\n"
                f"[{theme.bar_color(d['percent'])}]{frac:─<{w}}[/]\n\n"
                f"util [bold]{d['util_percent']:.0f}[/]%"
            )
        d = disk_src.collect()
        lines = []
        for p in d["partitions"][:4]:
            frac = "█" * int(p["percent"] / 100 * w)
            lines.append(f"{p['mountpoint']}: {p['used_gb']:.0f}G/{p['total_gb']:.0f}G {p['percent']:.0f}%")
            lines.append(f"[{theme.bar_color(p['percent'])}]{frac:─<{w}}[/]")
        return "\n".join(lines) + f"\n\nio {d['read_mb_s']:.1f}R / {d['write_mb_s']:.1f}W MB/s"

    def _refresh(self) -> None:
        self.query_one("#detail-gauges").update(self._gauge_text())
        table = self._table()
        table.clear()
        for row in self._rows():
            table.add_row(*row)
        d = {"cpu": cpu_src.collect, "ram": mem_src.collect, "disk": disk_src.collect, "gpu": gpu_src.collect}[self.kind]()
        self.query_one("#detail-footer").update(
            f"[dim #0f8038]live ▸ {self.label} {d.get('percent', 0):.1f}%[/]"
        )

    def _table(self) -> DataTable:
        return self.query_one(DataTable)

    def action_back(self) -> None:
        self.app.pop_screen()


def _mini_bars(values: list[float], width: int) -> str:
    """Compact horizontal per-core mini-bars."""
    out = []
    for i, v in enumerate(values):
        c = theme.bar_color(v)
        out.append(f"c{i}[{c}]{_bar(v, max(4, width // max(len(values), 1)))}[/{c}]")
    return "".join(out[: width // 12])


def _bar(percent: float, width: int) -> str:
    filled = round(percent / 100 * width)
    return "█" * filled + "·" * (width - filled)
