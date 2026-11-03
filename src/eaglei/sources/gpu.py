"""GPU collector — NVIDIA via nvidia-smi; degrades to {"available": False}."""

import shutil
import subprocess

GB = 1024**3
_BIN = shutil.which("nvidia-smi") or "/usr/bin/nvidia-smi"


def _qsmi(*args: str) -> str:
    try:
        r = subprocess.run([_BIN, *args], capture_output=True, text=True, timeout=3)
        return r.stdout
    except (subprocess.TimeoutExpired, OSError):
        return ""


def collect() -> dict:
    out = _qsmi("--query-gpu=name,memory.total,memory.used,utilization.gpu", "--format=csv,noheader,nounits")
    if not out.strip():
        return {"name": "gpu", "available": False}
    try:
        vname, total, used, util = [x.strip() for x in out.splitlines()[0].split(",")]
    except ValueError:
        return {"name": "gpu", "available": False}
    return {
        "name": "gpu",
        "available": True,
        "device": vname,
        "total_mb": float(total),
        "used_mb": float(used),
        "percent": round(float(used) / max(float(total), 1) * 100, 1),
        "util_percent": float(util),
    }


def top_processes(n: int = 15) -> list[dict]:
    """Processes holding VRAM, straight from nvidia-smi (requested earlier; works on this machine)."""
    out = _qsmi("--query-compute-apps=pid,used_memory,process_name", "--format=csv,noheader,nounits")
    rows = []
    for line in out.splitlines():
        try:
            pid, mem, pname = [x.strip() for x in line.split(",")]
            rows.append({"pid": int(pid), "name": pname.split("/")[-1][:40], "value": round(float(mem) / 1024, 2)})
        except ValueError:
            continue
    rows.sort(key=lambda r: r["value"], reverse=True)
    return rows[:n]
