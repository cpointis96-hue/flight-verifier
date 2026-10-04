"""Deterministic flight discovery and official-fare verification primitives."""

from .models import FlightCandidate, FlightSearchRequest, VerificationResult
from .orchestrator import FallbackOrchestrator

__all__ = ["FlightCandidate", "FlightSearchRequest", "VerificationResult", "FallbackOrchestrator"]
