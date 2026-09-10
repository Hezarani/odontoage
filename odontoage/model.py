"""Result data structures returned by OdontoAge estimators."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class Interval:
    """A prediction interval around an estimated age (in years)."""
    low: float
    high: float
    level: float = 0.95
    basis: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Estimate:
    """The outcome of applying one method to one individual.

    ``estimated_age_years`` is the point estimate. ``interval`` is an *approximate*
    prediction interval based on the method's reported standard error where one is
    published; it describes population-level dispersion, not a per-individual
    guarantee. Always read ``disclaimer`` and ``warnings``.
    """
    method: str
    label: str
    estimated_age_years: Optional[float]
    dentition: str
    sex: Optional[str] = None
    interval: Optional[Interval] = None
    maturity_score: Optional[float] = None
    reasoning: List[str] = field(default_factory=list)
    inputs: Dict[str, Any] = field(default_factory=dict)
    citation: str = ""
    doi: Optional[str] = None
    disclaimer: str = ""
    warnings: List[str] = field(default_factory=list)
    verified: bool = True

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if self.interval is not None:
            d["interval"] = self.interval.to_dict()
        return d

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        if self.estimated_age_years is None:
            head = f"{self.label}: (no point estimate)"
        else:
            head = f"{self.label}: {self.estimated_age_years:.2f} y"
            if self.interval is not None:
                head += f" (95% ~ {self.interval.low:.2f}-{self.interval.high:.2f} y)"
        return head
