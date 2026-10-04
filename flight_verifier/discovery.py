from typing import Protocol

from .models import FlightCandidate, FlightSearchRequest


class DiscoveryProvider(Protocol):
    name: str

    def search(self, request: FlightSearchRequest) -> list[FlightCandidate]: ...
