"""Finite-sample bounds for fixed policies evaluated across independent assignment groups."""

import numpy as np


def hoeffding_radius(widths: np.ndarray, alpha: float) -> float:
    if len(widths) == 0 or not np.isfinite(widths).all() or np.any(widths < 0) or not 0 < alpha < 1:
        raise ValueError("Finite nonnegative range widths and a valid tail probability are required")
    return float(np.sqrt(np.square(widths).sum() * np.log(2 / alpha) / 2) / len(widths))
