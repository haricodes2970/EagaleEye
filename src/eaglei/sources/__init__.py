"""System data sources. Each module exposes a `collect()` returning plain dicts.

Sources are hardware-facing ONLY: they talk to psutil / nvidia-smi and return
numbers. Screens and charts never import psutil directly.
"""
