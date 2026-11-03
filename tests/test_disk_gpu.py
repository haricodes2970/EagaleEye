"""Tests for disk + gpu sources (hardware-tolerant, run anywhere)."""

from eaglei.sources import disk, gpu


def test_disk_collect_shape():
    d = disk.collect()
    assert d["name"] == "disk"
    assert d["total_gb"] > 0
    assert 0 <= d["percent"] <= 100
    assert isinstance(d["partitions"], list) and d["partitions"]
    p = d["partitions"][0]
    assert {"device", "mountpoint", "percent"} <= set(p)


def test_disk_io_rate_keys():
    d = disk.collect()
    assert d["read_mb_s"] >= 0.0 and d["write_mb_s"] >= 0.0


def test_gpu_collect_shape():
    d = gpu.collect()
    assert d["name"] == "gpu"
    if d["available"]:
        assert 0 <= d["percent"] <= 100
        assert d["used_mb"] <= d["total_mb"]
        assert "device" in d
