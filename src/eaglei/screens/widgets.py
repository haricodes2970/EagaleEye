"""Wing — one focused-on-metric card: a poller + a swappable chart renderer."""

from collections import deque

from textual.app import ComposeResult
from textual.widgets import Static

from .. import charts
from ..sources import cpu, disk, gpu, memory

LABELS = {"cpu": "CPU", "ram": "RAM", "disk": "DISK", "gpu": "GPU"}
COLLECT = {
    "cpu": cpu.collect,
    "ram": memory.collect,
    "disk": disk.collect,
    "gpu": gpu.collect,
}
#: per-metric poll ticks (seconds)
INTERVALS = {"cpu": 1.0, "ram": 1.0, "disk": 3.0, "gpu": 1.0}


class Wing(Static, can_focus=True):
    """Card bound to one source; `chart_type` renders via charts registry."""

    def __init__(self, kind: str, chart_type: str) -> None:
        super().__init__(classes=f"wing wing-{kind}", id=f"wing-{kind}")
        self.kind = kind
        self.chart_type = chart_type
        self.history: deque[float] = deque(maxlen=64)
        self._data: dict = {}

    def on_mount(self) -> None:
        self.border_title = LABELS[self.kind]
        self.set_interval(INTERVALS[self.kind], self._tick)
        self._tick()

    def on_click(self) -> None:
        """Click a wing → focus it, then drill down (Task-Manager view)."""
        self.focus()
        self.app.action_drill()

    def _tick(self) -> None:
        d = COLLECT[self.kind]()
        d["label"] = LABELS[self.kind]
        if self.kind == "cpu":
            d["rows"] = [
                (f"c{(i % 8)}", v, "")
                for i, v in enumerate(d.get("per_core", [])[:8])
                if v > 1.0
            ] or [("cpu", d["percent"], "all cores idle")]
        elif self.kind == "ram":
            d["rows"] = [
                ("used", d["percent"], f"{d['used_gb']:.1f}G/{d['total_gb']:.0f}G"),
                ("swap", d["swap_percent"], f"{d['swap_used_gb']:.1f}G"),
            ]
        elif self.kind == "gpu" and d.get("available"):
            d["rows"] = [
                ("vram", d["percent"], f"{d['used_mb']:.0f}MB"),
                ("util", d.get("util_percent", 0), ""),
            ]

        # numeric-ledger fields per wing (free/occupied/running counts)
        if self.kind == "cpu":
            pc = d.get("per_core", [])
            busy = [v for v in pc if v > 1.0]
            hottest = max(pc) if pc else 0.0
            d["fields"] = [
                ("load", f"{d['percent']:.1f}%", d["percent"]),
                ("hot core", f"{hottest:.1f}%", hottest),
                ("busy cores", f"{len(busy)}/{d['cores']}"),
                ("freq", f"{d['freq_mhz']:.0f} of {d['freq_max_mhz']:.0f} MHz"),
                ("load avg", "/".join(f"{x:.1f}" for x in d["load_avg"][:3])),
                ("procs running", str(d.get("nproc", "?"))),
            ]
        elif self.kind == "ram":
            d["fields"] = [
                ("occupied", f"{d['used_gb']:.1f}G / {d['total_gb']:.1f}G", d["percent"]),
                ("free", f"{d['available_gb']:.1f}G", 100 - d["percent"]),
                ("swap used", f"{d['swap_used_gb']:.1f}G / {d['swap_total_gb']:.0f}G", d["swap_percent"]),
                ("procs alive", str(d.get("nproc", "?"))),
            ]
        elif self.kind == "disk":
            fields = [
                ("occupied", f"{d['used_gb']:.0f}G / {d['total_gb']:.0f}G", d["percent"]),
                ("free", f"{round(d['total_gb'] - d['used_gb'], 1)}G", 100 - d["percent"]),
            ]
            for p in d.get("partitions", [])[:3]:
                fields.append((f"{p['mountpoint'][-8:] or '/'}", f"{p['used_gb']:.0f}G/{p['total_gb']:.0f}G", p["percent"]))
            fields += [
                ("io read", f"{d['read_mb_s']:.1f} MB/s"),
                ("io write", f"{d['write_mb_s']:.1f} MB/s"),
            ]
            d["fields"] = fields
        elif self.kind == "gpu" and d.get("available"):
            holders = gpu.top_processes(64)
            d["fields"] = [
                ("occupied", f"{d['used_mb']:.0f} / {d['total_mb']:.0f} MB", d["percent"]),
                ("free", f"{d['total_mb'] - d['used_mb']:.0f} MB", 100 - d["percent"]),
                ("util", f"{d.get('util_percent', 0):.0f}%", d.get("util_percent", 0)),
                ("vram procs", str(len(holders))),
            ]
        self._data = d
        self.history.append(d.get("percent", 0.0))
        self.refresh()

    def _caption_pad(self, d: dict) -> dict:
        """Chart context per wing (severity hints, io captions...)."""
        return d

    def render(self) -> str:
        d = dict(self._data)
        d["history"] = list(self.history)
        d.setdefault("label", LABELS[self.kind])
        if self.kind == "disk" and d.get("partitions"):
            d["rows"] = [(p["mountpoint"].rstrip("/") or "/", p["percent"], "") for p in d["partitions"]][:3]
        fn = charts.CHARTS[self.chart_type]
        w = max(self.size.width or 40, 12)
        h = max(self.size.height or 10, 6)
        try:
            body = fn(d, w, h - 1)
            # vertical centering: short charts read better floating mid-card
            lines = body.splitlines()
            gap = max(0, (h - 1) - len(lines))
            if gap:
                body = "\n".join([""] * (gap // 2) + lines)
        except Exception as exc:  # chart crash never kills the hawk
            body = f"[alert]chart error: {exc}[/alert]"
        return body
