import unittest
from datetime import date

from flight_verifier.models import FlightSearchRequest


class ModelTests(unittest.TestCase):
    def test_rejects_invalid_search_request(self):
        with self.assertRaises(ValueError):
            FlightSearchRequest("", "HYD", date(2026, 10, 7))
        with self.assertRaises(ValueError):
            FlightSearchRequest("CMB", "HYD", date(2026, 10, 7), passengers=0)

    def test_rejects_return_before_departure(self):
        with self.assertRaises(ValueError):
            FlightSearchRequest("CMB", "HYD", date(2026, 10, 7), date(2026, 10, 6))


if __name__ == "__main__":
    unittest.main()
