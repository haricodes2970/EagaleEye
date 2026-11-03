"""Tests for hardware-facing sources (cpu, memory)."""

from eaglei.sources import cpu, memory


def test_cpu_collect_shape():
    d = cpu.collect()
    assert d["name"] == "cpu"
    assert 0.0 <= d["percent"] <= 100.0
    assert len(d["per_core"]) == d["cores"]
    assert d["cores"] >= 1
    assert len(d["load_avg"]) >= 2


def test_memory_collect_shape():
    d = memory.collect()
    assert d["name"] == "ram"
    assert d["total_gb"] > 0
    assert d["used_gb"] <= d["total_gb"]
    assert 0.0 <= d["percent"] <= 100.0
    assert d["swap_total_gb"] >= 0


def test_top_processes_cpu():
    rows = cpu.top_processes(5)
    assert len(rows) <= 5
    assert all({"pid", "name", "value"} <= set(r) for r in rows)


def test_top_processes_memory_sorted():
    rows = memory.top_processes(8)
    values = [r["value"] for r in rows]
    assert values == sorted(values, reverse=True)
    assert all(r["value"] > 0 for r in rows)
