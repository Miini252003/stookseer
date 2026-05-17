from __future__ import annotations

from typing import Iterable, List


def normalize_prices(prices: Iterable[float], base_value: float = 100.0) -> List[float]:
    values = [float(p) for p in prices]
    if not values:
        return []

    base = values[0]
    if base == 0:
        base = 1e-9
    return [round((p / base) * base_value, 4) for p in values]
