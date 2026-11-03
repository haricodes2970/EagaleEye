"""Disk collector — partitions, usage, read/write throughput (needs a baseline tick)."""

import psutil

GB = 1024**3
_prev_io: dict = {}  # device -> (read_bytes, write_bytes)


def collect() -> dict:
    parts = []
    total_used = total_size = 0
    for p in psutil.disk_partitions(all=False):
        try:
            u = psutil.disk_usage(p.mountpoint)
        except (PermissionError, OSError):
            continue
        if p.fstype in ("squashfs", "tmpfs", "devtmpfs"):
            continue
        total_used += u.used
        total_size += u.total
        parts.append(
            {
                "device": p.device,
                "mountpoint": p.mountpoint,
                "total_gb": round(u.total / GB, 1),
                "used_gb": round(u.used / GB, 1),
                "free_gb": round(u.free / GB, 1),
                "percent": round(u.percent, 1),
            }
        )

    io = psutil.disk_io_counters()  # aggregate across devices
    rps = wps = 0.0
    if io:
        rps, wps = _delta_rate("<>(total)", io.read_bytes, io.write_bytes)
    return {
        "name": "disk",
        "partitions": parts,
        "total_gb": round(total_size / GB, 1),
        "used_gb": round(total_used / GB, 1),
        "percent": round(100 * total_used / max(total_size, 1), 1),
        "read_mb_s": round(rps / 1024**2, 1),
        "write_mb_s": round(wps / 1024**2, 1),
    }


def _delta_rate(key: str, read_bytes: int, write_bytes: int) -> tuple[float, float]:
    """ns of rate computation as eased."""
    prev = _prev_io.get(key)
    _prev_io[key] = (read_bytes, write_bytes)
    if prev is None:
        return 0.0, 0.0
    return read_bytes - prev[0], write_bytes - prev[1]
