"""Prospective comparison of two frozen strategies at matched capacity."""
from dataclasses import dataclass
from math import ceil, isfinite, sqrt
from statistics import NormalDist

NORMAL = NormalDist()


@dataclass(frozen=True)
class Pilot:
    baseline: float
    effect: float
    capacity: float
    concentration: float
    capture: float
    allocation: float
    alpha: float
    attrition: float = 0.0
    cluster_size: float = 1.0
    icc: float = 0.0

    def rates(self) -> tuple[float, float]:
        """Return uniform and targeted rates in the two policy arms."""
        values = tuple(vars(self).values())
        if not all(isfinite(value) for value in values):
            raise ValueError("All inputs must be finite.")
        if not (0 < self.baseline < 1 and 0 < self.capacity <= 1
                and self.concentration >= 1 and 0 <= self.capture <= 1
                and 0 < self.allocation < 1 and 0 < self.alpha < 1
                and 0 <= self.attrition < 1 and self.cluster_size >= 1 and 0 <= self.icc < 1):
            raise ValueError("Pilot assumptions are out of range.")
        if self.capacity == 1:
            high = low = self.effect
        else:
            high = self.concentration * self.effect
            low = (self.effect - self.capacity * high) / (1 - self.capacity)
        if not all(0 <= self.baseline + tau <= 1 for tau in (high, low)):
            raise ValueError("The assumptions imply an impossible subgroup outcome rate.")
        uniform = self.baseline + self.capacity * self.effect
        targeted = uniform + self.capacity * self.capture * (high - self.effect)
        return uniform, targeted

    def variance(self) -> float:
        uniform, targeted = self.rates()
        variance = uniform * (1 - uniform) / (1 - self.allocation)
        variance += targeted * (1 - targeted) / self.allocation
        return variance * (1 + (self.cluster_size - 1) * self.icc) / (1 - self.attrition)

    def power(self, enrollment: int) -> float:
        if type(enrollment) is not int or enrollment < 2:
            raise ValueError("Enrollment must be an integer of at least 2.")
        uniform, targeted = self.rates()
        if uniform == targeted:
            return self.alpha
        shift = abs(targeted - uniform) * sqrt(enrollment / self.variance())
        z = NORMAL.inv_cdf(1 - self.alpha / 2)
        return NORMAL.cdf(shift - z) + NORMAL.cdf(-shift - z)

    def enrollment(self, target: float) -> int | None:
        if not self.alpha < target < 1:
            raise ValueError("Target power must be between alpha and 100%.")
        uniform, targeted = self.rates()
        if uniform == targeted:
            return None
        lower, upper = 0.0, 20.0
        z = NORMAL.inv_cdf(1 - self.alpha / 2)
        for _ in range(56):
            shift = (lower + upper) / 2
            if NORMAL.cdf(shift - z) + NORMAL.cdf(-shift - z) < target:
                lower = shift
            else:
                upper = shift
        return max(2, ceil(upper**2 * self.variance() / (targeted - uniform)**2))
