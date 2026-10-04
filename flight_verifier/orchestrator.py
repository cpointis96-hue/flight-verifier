from .errors import HumanInterventionRequired, VerificationError
from .models import Attempt, VerificationResult


class FallbackOrchestrator:
    """Run verification layers once, from least expensive to most expensive."""

    def __init__(self, layers, max_attempts=1):
        if max_attempts != 1:
            raise ValueError("only one bounded attempt per layer is supported")
        self.layers = tuple(layers)

    def verify(self, request, candidate):
        attempts = []
        for layer in self.layers:
            try:
                result = layer.verify(request, candidate)
                if not isinstance(result, VerificationResult):
                    raise TypeError("verification layer must return VerificationResult")
                return result.with_attempts(attempts + [Attempt(layer.name, "success")] + list(result.attempts))
            except HumanInterventionRequired as error:
                attempts.append(Attempt(layer.name, str(error)))
                return VerificationResult(candidate, layer.name, attempts=tuple(attempts), human_intervention_required=True)
            except (VerificationError, TimeoutError, ConnectionError) as error:
                attempts.append(Attempt(layer.name, str(error)))
        return VerificationResult(candidate, "fallback-exhausted", attempts=tuple(attempts))
