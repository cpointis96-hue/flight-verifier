from typing import Any, Protocol

from ..models import FlightCandidate, FlightSearchRequest, VerificationResult


class OfficialSiteClient(Protocol):
    def verify_fare(self, request: FlightSearchRequest, candidate: FlightCandidate) -> dict[str, Any]: ...


class OfficialAirlineAdapter:
    airline_code = ""

    def __init__(self, client: OfficialSiteClient):
        self.client = client
        self.name = f"official:{self.airline_code.lower()}"

    def verify(self, request, candidate) -> VerificationResult:
        payload = self.client.verify_fare(request, candidate)
        return self.map_payload(candidate, payload)

    def map_payload(self, candidate, payload) -> VerificationResult:
        raise NotImplementedError
