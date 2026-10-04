from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum


class EvidenceLevel(str, Enum):
    OBSERVED = "observed"
    OFFICIAL_PUBLISHED = "official_published"
    CALCULATED = "calculated"
    UNVERIFIED = "unverified"


@dataclass(frozen=True)
class FlightSearchRequest:
    origin: str
    destination: str
    departure_date: date
    return_date: date | None = None
    passengers: int = 1
    cabin: str = "economy"

    def __post_init__(self):
        if not self.origin.strip() or not self.destination.strip():
            raise ValueError("origin and destination are required")
        if self.passengers < 1:
            raise ValueError("passengers must be at least 1")
        if self.return_date and self.return_date < self.departure_date:
            raise ValueError("return_date cannot precede departure_date")


@dataclass(frozen=True)
class FlightCandidate:
    airline: str
    flight_number: str | None
    origin: str
    destination: str
    currency: str | None = None
    price: float | None = None
    departure: str | None = None
    arrival: str | None = None
    fare_name: str | None = None
    official_source: str | None = None
    observed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class Attempt:
    layer: str
    error: str


@dataclass(frozen=True)
class VerificationResult:
    candidate: FlightCandidate
    source: str
    verified: bool = False
    evidence_level: EvidenceLevel = EvidenceLevel.UNVERIFIED
    refund_conditions: str | None = None
    refund_fee: str | None = None
    refund_amount_or_percentage: str | None = None
    change_conditions: str | None = None
    baggage: str | None = None
    verified_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    attempts: tuple[Attempt, ...] = ()
    human_intervention_required: bool = False

    def with_attempts(self, attempts, human_intervention_required=False):
        return VerificationResult(**{**self.__dict__, "attempts": tuple(attempts), "human_intervention_required": human_intervention_required})
