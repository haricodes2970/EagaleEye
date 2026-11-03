"""Chart kit. Six visualizations, one duck-typed contract.

Every module exposes `render(data, width, height) -> str` with rich markup
inline. Registry + shuffle live here. Charts are dumb: they only read numbers.
"""
import random

from .gauge import render as gauge
from .graph import render as graph
from .hbar import render as bar
from .numeric import render as numeric
from .pie import render as pie
from .radial import render as radial
from .sparkline import render as sparkline

#: chart-type name -> render fn
CHARTS: dict[str, object] = {
    "bar": bar,
    "numbers": numeric,
    "pie": pie,
    "sparkline": sparkline,
    "gauge": gauge,
    "radial": radial,
    "graph": graph,
}

ORDER = list(CHARTS)  # dock display order (1..6 keys)


def shuffle(count: int, seed: int | None = None) -> list[str]:
    """Random chart-type per wing; `seed` makes the session reproducible."""
    rng = random.Random(seed)
    return [rng.choice(ORDER) for _ in range(count)]
