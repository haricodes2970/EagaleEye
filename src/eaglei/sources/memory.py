"""Memory collector — RAM, swap/zram, top consumers by RSS."""

import psutil

GB = 1024**3


def collect() -> dict:
    v = psutil.virtual_memory()
    s = psutil.swap_memory()
    return {
        "name": "ram",
        "total_gb": round(v.total / GB, 2),
        "used_gb": round(v.used / GB, 2),
        "available_gb": round(v.available / GB, 2),
        "percent": round(v.percent, 1),
        "swap_total_gb": round(s.total / GB, 2),
        "swap_used_gb": round(s.used / GB, 2),
        "swap_percent": round(s.percent, 1),
        "nproc": len(psutil.pids()),
    }


def top_processes(n: int = 15) -> list[dict]:
    """Top processes by resident memory (Task-Manager RAM column)."""
    procs = []
    for p in psutil.process_iter(["pid", "name", "memory_info"]):
        info = p.info
        mi = info["memory_info"]
        if mi is None:
            continue
        procs.append(
            {
                "pid": info["pid"],
                "name": (info["name"] or "?")[:40],
                "value": round(mi.rss / GB, 2),
            }
        )
    procs.sort(key=lambda r: r["value"], reverse=True)
    return procs[:n]
