import unittest
from datetime import date

from flight_verifier.adapters.sri_lankan import SriLankanAdapter
from flight_verifier.models import EvidenceLevel, FlightCandidate, FlightSearchRequest


class FixtureClient:
    def __init__(self, payload):
        self.payload = payload

    def verify_fare(self, request, candidate):
        return self.payload


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.request = FlightSearchRequest("CMB", "HYD", date(2026, 10, 7))
        self.candidate = FlightCandidate("SriLankan Airlines", "UL177", "CMB", "HYD", "LKR", 147666)

    def test_maps_official_fare_payload_without_network(self):
        payload = {
            "fare_name": "BIZ VALUE",
            "official_source": "https://digital.srilankan.com/",
            "refund_conditions": "Before departure: permitted with restrictions; after departure: not permitted.",
            "refund_fee": "Up to 28,800 LKR",
            "refund_amount_or_percentage": "Estimated net: total less applicable penalty and taxes.",
            "change_conditions": "Date/time changes not permitted; routing changes permitted with restrictions.",
            "baggage": "40 kg checked; 2 x 7 kg cabin",
        }
        result = SriLankanAdapter(FixtureClient(payload)).verify(self.request, self.candidate)

        self.assertTrue(result.verified)
        self.assertEqual(result.evidence_level, EvidenceLevel.OBSERVED)
        self.assertIn("28,800", result.refund_fee)
        self.assertEqual(result.baggage, "40 kg checked; 2 x 7 kg cabin")


if __name__ == "__main__":
    unittest.main()
