"""OdontoAge — an open, cross-verified reference implementation of dental
age-estimation methods (Cameriere, Demirjian, Willems, Kvaal).

Research/education only. Read ``GENERAL_DISCLAIMER`` before use.
"""
from . import errors
from .core import GENERAL_DISCLAIMER, compare, estimate, list_methods
from .model import Estimate, Interval

__version__ = "0.1.0"

__all__ = [
    "estimate",
    "compare",
    "list_methods",
    "Estimate",
    "Interval",
    "errors",
    "GENERAL_DISCLAIMER",
    "__version__",
]
