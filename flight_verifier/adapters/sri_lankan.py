from ..errors import HumanInterventionRequired, VerificationUnavailable
from dataclasses import replace

from ..models import EvidenceLevel, VerificationResult
from .base import OfficialAirlineAdapter


class SriLankanAdapter(OfficialAirlineAdapter):
    airline_code = "UL"

    def map_payload(self, candidate, payload):
        if payload.get("human_intervention_required"):
            raise HumanInterventionRequired(payload.get("message", "official site requires human intervention"))
        if not payload.get("official_source") or not payload.get("fare_name"):
            raise VerificationUnavailable("SriLankan payload lacks fare identity or official source")
        return VerificationResult(
            candidate=replace(candidate, fare_name=payload["fare_name"], official_source=payload["official_source"]),
            source=payload["official_source"],
            verified=True,
            evidence_level=EvidenceLevel.OBSERVED,
            refund_conditions=payload.get("refund_conditions"),
            refund_fee=payload.get("refund_fee"),
            refund_amount_or_percentage=payload.get("refund_amount_or_percentage"),
            change_conditions=payload.get("change_conditions"),
            baggage=payload.get("baggage"),
        )
