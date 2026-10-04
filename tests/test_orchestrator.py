import unittest
from datetime import date

from flight_verifier.errors import HumanInterventionRequired, VerificationUnavailable
from flight_verifier.models import FlightCandidate, FlightSearchRequest, VerificationResult
from flight_verifier.orchestrator import FallbackOrchestrator


REQUEST = FlightSearchRequest("CMB", "HYD", date(2026, 10, 7))
CANDIDATE = FlightCandidate("SriLankan Airlines", "UL177", "CMB", "HYD", "LKR", 147666)


class Layer:
    def __init__(self, name, outcome):
        self.name = name
        self.outcome = outcome
        self.calls = 0

    def verify(self, request, candidate):
        self.calls += 1
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return self.outcome


class FallbackOrchestratorTests(unittest.TestCase):
    def test_tries_layers_in_order_and_stops_after_success(self):
        structured = Layer("structured", VerificationUnavailable("no endpoint"))
        playwright = Layer("playwright", VerificationResult(candidate=CANDIDATE, source="official", verified=True))

        result = FallbackOrchestrator([structured, playwright]).verify(REQUEST, CANDIDATE)

        self.assertTrue(result.verified)
        self.assertEqual([a.layer for a in result.attempts], ["structured", "playwright"])
        self.assertEqual(playwright.calls, 1)

    def test_does_not_retry_a_layer_by_default(self):
        layer = Layer("structured", VerificationUnavailable("temporary"))

        result = FallbackOrchestrator([layer]).verify(REQUEST, CANDIDATE)

        self.assertFalse(result.verified)
        self.assertEqual(layer.calls, 1)
        self.assertEqual(result.attempts[0].error, "temporary")

    def test_human_intervention_stops_the_chain(self):
        human = Layer("playwright", HumanInterventionRequired("captcha"))
        last = Layer("computer-use", VerificationResult(candidate=CANDIDATE, source="visual", verified=True))

        result = FallbackOrchestrator([human, last]).verify(REQUEST, CANDIDATE)

        self.assertFalse(result.verified)
        self.assertTrue(result.human_intervention_required)
        self.assertEqual(last.calls, 0)


if __name__ == "__main__":
    unittest.main()
