"""Exception types for OdontoAge."""


class OdontoAgeError(Exception):
    """Base class for all OdontoAge errors."""


class UnknownMethodError(OdontoAgeError):
    """Raised when a requested method id is not registered."""


class MethodNotVerifiedError(OdontoAgeError):
    """Raised when a method's encoded parameters have not been cross-verified.

    OdontoAge refuses to produce an age from parameters that have not been
    confirmed against >=2 independent authoritative sources, because a wrong
    constant in a forensic tool is worse than no tool at all. Pass
    ``allow_unverified=True`` only for development/inspection.
    """


class InvalidInputError(OdontoAgeError):
    """Raised when the inputs for a method are missing or malformed."""
