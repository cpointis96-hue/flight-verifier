class VerificationError(Exception):
    """Base class for bounded verification failures."""


class VerificationUnavailable(VerificationError):
    """The current layer cannot provide a reliable result."""


class HumanInterventionRequired(VerificationError):
    """The site requires a human action; automation must stop."""
