"""Boot fetch screen — eagle art left, structured hardware ledger right.

Copies the look of your reference screenshots (lotus/spider fetch) but with
the EAGLE as the glyph mascot, neon-green hacker theme.  Any key / click
drops into the live dashboard; Esc returns here.
"""

import datetime
import os

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static

from .. import theme
from ..art.eagle import EAGLE, EAGLE_SMALL, RAMP_STRIPES
from ..sources import cpu as cpu_src
from ..sources import disk as disk_src
from ..sources import memory as mem_src
from ..sources import gpu as gpu_src


def _bar_line(label: str, used: str, total: str, pct: float, width: int) -> str:
    """One resource row: label ░███░░ value/total pct%"""
    c = theme.bar_color(pct)
    filled = round(pct / 100 * max(width - 30, 10))
    bar = f"[{c}]{'█' * filled}[/{c}][{theme.DIM}]{'░' * (max(width - 30, 10) - filled)}[/{theme.DIM}]"
    return f"[{theme.DIM}]{label:<7}[/]  {bar}  [{theme.FG}]{used}[/] / [{theme.FG}]{total}[/]  [bold {c}]{pct:4.1f}%[/bold]"


class EagleColumn(Static):
    """Left column: eagle glyph with per-row neon-gradient stripes."""

    def render(self) -> str:
        lines: list[str] = []
        for idx, row in enumerate(EAGLE):
            if not row.strip():
                lines.append("")
                continue
            color = RAMP_STRIPES[min(idx, len(RAMP_STRIPES) - 1)]
            tinted = "".join(
                f"[{color}]{ch}[/]" if ch != " " else ch for ch in row
            )
            lines.append(tinted)
        return "\n".join(lines)


class HeaderBand(Static):
    """Top-right banner: hawk logo + hello."""

    def on_mount(self) -> None:
        self.set_interval(1.0, self.refresh_now)
        self.refresh_now()

    def refresh_now(self) -> None:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        host = os.uname().nodename
        self.update(
            f"[bold {theme.FG}]{EAGLE_SMALL} EAGLE EYE[/bold {theme.FG}]  [dim {theme.DIM}]— {host} · {now}[/]"
        )


class HardwarePanel(Static):
    """CPU / GPU / RAM / SWAP / DRIVE ledger rows."""

    def render(self) -> str:
        rows: list[str] = []
        cpu_d = cpu_src.collect()
        ram_d = mem_src.collect()
        gpu_d = gpu_src.collect()
        disk_d = disk_src.collect()

        rows.append(
            f"[{theme.DIM}]CPU[/]  [{theme.FG}]{cpu_d['percent']:4.1f}%[/]  "
            f"[{theme.bar_color(cpu_d['percent'])}]{'█'*int(cpu_d['percent']/5)}[/]"
        )
        rows.append(f"    [{theme.DIM}]model[/] {cpu_d.get('model', '?')}  "
                    f"[{theme.DIM}]{cpu_d['cores']}c @ {cpu_d['freq_mhz']:.0f} MHz[/]")
        rows.append("")

        if gpu_d.get("available"):
            rows.append(
                f"[{theme.DIM}]GPU[/]  [{theme.FG}]{gpu_d['percent']:4.1f}%[/]  "
                f"[{theme.bar_color(gpu_d['percent'])}]{'█'*int(gpu_d['percent']/5)}[/]"
            )
            rows.append(
                f"    [{theme.DIM}]model[/] {gpu_d.get('device', '?')}  "
                f"[{theme.DIM}]VRAM {gpu_d['used_mb']:.0f}/{gpu_d['total_mb']:.0f} MB[/]"
            )
        else:
            rows.append(f"[{theme.DIM}]GPU[/]  [dim {theme.DIM}]no NVIDIA GPU detected[/]")
        rows.append("")

        rows.append(
            f"[{theme.DIM}]RAM[/]  [{theme.FG}]{ram_d['percent']:4.1f}%[/]  "
            f"[{theme.bar_color(ram_d['percent'])}]{'█'*int(ram_d['percent']/5)}[/]"
        )
        rows.append(
            f"    [{theme.DIM}]used[/] {ram_d['used_gb']:.1f} GB  "
            f"[{theme.DIM}]total[/] {ram_d['total_gb']:.1f} GB"
        )
        rows.append("")

        rows.append(
            f"[{theme.DIM}]SWAP[/]  [{theme.FG}]{ram_d['swap_percent']:4.1f}%[/]  "
            f"[{theme.bar_color(ram_d['swap_percent'])}]{'█'*int(ram_d['swap_percent']/5)}[/]"
        )
        rows.append(
            f"    [{theme.DIM}]used[/] {ram_d['swap_used_gb']:.1f} GB  "
            f"[{theme.DIM}]total[/] {ram_d['swap_total_gb']:.1f} GB"
        )
        rows.append("")

        for p in disk_d.get("partitions", [])[:4]:
            label = p["mountpoint"].rstrip("/") or "/"
            rows.append(
                f"[{theme.DIM}]DRIVE[/]  [{theme.FG}]{p['percent']:4.1f}%[/]  "
                f"[{theme.bar_color(p['percent'])}]{'█'*int(p['percent']/5)}[/]"
            )
            rows.append(
                f"    [{theme.DIM}]mount[/] {label}  "
                f"[{theme.DIM}]used {p['used_gb']:.0f}/{p['total_gb']:.0f} GB[/]"
            )
        rows.append("")

        return "\n".join(rows)


class SessionPanel(Static):
    def render(self) -> str:
        return (
            f"[{theme.FG}]LOGIN[/]  [{theme.DIM}]{os.getlogin()}[/]  "
            f"[dim {theme.DIM}]// {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/]\n"
            f"[{theme.FG}]UPTIME[/]  [{theme.DIM}]{self._uptime()}[/]\n"
            f"[{theme.FG}]DATE[/]   [{theme.DIM}]{datetime.date.today().isoformat()}[/]"
        )

    @staticmethod
    def _uptime() -> str:
        try:
            with open("/proc/uptime") as f:
                secs = float(f.read().split()[0])
            return f"{int(secs // 3600)}h {int((secs % 3600) // 60):02d}m"
        except OSError:
            return "unknown"


class PaletteRow(Static):
    COLORS = ["#1a1a1a", "#063014", "#0f6b2b", "#1fb84a", "#00ff41", "#2bff60", "#ff3341", "#ffd633"]

    def render(self) -> str:
        dots = "  ".join(f"[{c}]●[/]" for c in self.COLORS)
        return dots


class FetchScreen(Screen):
    """Boot screen — eagle + hardware ledger. Key/click → dashboard."""

    BINDINGS = [
        ("escape", "back", "Return to fetch"),
        ("d", "dash", "Dashboard"),
        ("enter", "dash", "Dashboard"),
        ("space", "dash", "Dashboard"),
    ]

    def compose(self) -> ComposeResult:
        yield HeaderBand(id="fetch-header")
        with Horizontal(id="fetch-body"):
            yield Vertical(EagleColumn(), id="eagle-column")
            with Vertical(id="panel-column"):
                yield HardwarePanel(id="panel-hardware")
                yield SessionPanel(id="panel-session")
                yield PaletteRow(id="panel-palette")

    def on_mount(self) -> None:
        # hardware panel refreshes live while on fetch too
        self.set_interval(1.0, lambda: self.query_one("#panel-hardware").refresh())
        self.set_interval(1.0, lambda: self.query_one("#panel-session").refresh())

    def action_back(self) -> None:
        self.app.pop_screen()

    def action_dash(self) -> None:
        self.app.push_screen("overview")

    def on_click(self) -> None:
        self.action_dash()
