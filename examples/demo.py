"""Exercise the adapter with a local fixture; no live flight search."""

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path

from flight_verifier.adapters.sri_lankan import SriLankanAdapter
from flight_verifier.models import FlightCandidate, FlightSearchRequest
from flight_verifier.orchestrator import FallbackOrchestrator


class FixtureClient:
    def verify_fare(self, request, candidate):
        fixture = Path(__file__).resolve().parents[1] / "tests/fixtures/sri_lankan_biz_value.json"
        return json.loads(fixture.read_text(encoding="utf-8"))


def main():
    request = FlightSearchRequest("CMB", "HYD", date(2026, 10, 7))
    candidate = FlightCandidate("SriLankan Airlines", "UL177", "CMB", "HYD")
    result = FallbackOrchestrator([SriLankanAdapter(FixtureClient())]).verify(request, candidate)
    print(json.dumps({"demo_only": True, "live_site_checked": False, "result": asdict(result)}, default=str, indent=2))


if __name__ == "__main__":
    main()
