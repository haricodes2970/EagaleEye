"""Chart kit. Every module exposes `render(data, width, height) -> str`."""
import random

from .area import render as area
from .gauge import render as gauge
from .graph import render as graph
from .hbar import render as bar
from .heatmap import render as heatmap
from .histogram import render as histogram
from .numeric import render as numeric
from .pie import render as pie
from .radial import render as radial
from .scatter import render as scatter
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
    "area": area,
    "scatter": scatter,
    "heatmap": heatmap,
    "histogram": histogram,
}

ORDER: list[str] = list(CHARTS)  # dock order 1..len


def shuffle(count: int, seed: int | None = None) -> list[str]:
    """Random chart-type per wing; `seed` makes the session reproducible."""
    rng = random.Random(seed)
    return [rng.choice(ORDER) for _ in range(count)]
