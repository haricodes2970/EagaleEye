"""CPU collector — totals, per-core, frequency, load average."""

import psutil


def collect() -> dict:
    cores = psutil.cpu_percent(interval=None, percpu=True)
    freq = psutil.cpu_freq()
    return {
        "name": "cpu",
        "percent": round(sum(cores) / max(len(cores), 1), 1),
        "per_core": [round(c, 1) for c in cores],
        "cores": len(cores),
        "freq_mhz": round(freq.current, 0) if freq else 0,
        "freq_max_mhz": round(freq.max, 0) if freq and freq.max else 0,
        "load_avg": [round(x, 2) for x in psutil.getloadavg()],
    }


def top_processes(n: int = 15) -> list[dict]:
    """Top processes by CPU% (normalized per-core like `top`)."""
    ncpu = psutil.cpu_count() or 1
    procs = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent"]):
        info = p.info
        procs.append(
            {
                "pid": info["pid"],
                "name": (info["name"] or "?")[:40],
                "value": round((info["cpu_percent"] or 0) / ncpu, 1),
            }
        )
    procs.sort(key=lambda r: r["value"], reverse=True)
    return procs[:n]
