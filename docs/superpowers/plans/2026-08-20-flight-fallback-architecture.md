# Flight Verification Fallback Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a small, deterministic fallback orchestration core so Google Flights remains discovery-first and official-airline verification can evolve from structured data to browser adapters, with Computer Use last.

**Architecture:** Define typed, provider-neutral flight candidate and verification contracts. A bounded orchestrator tries layers in order, records failures, and stops on explicit human-intervention requirements. Airline adapters implement only the official verification contract; browser engines are injected, so no GUI automation is required by the core.

**Tech Stack:** Python 3.11+, standard library (`dataclasses`, `enum`, `typing`, `datetime`, `urllib`), `unittest`.

**Spec:** `project.md`

## Global Constraints

- Google Flights is the first discovery source; official airline sources are required for final fare verification.
- Computer Use is last resort only; no CAPTCHA, authentication, identity, payment, or purchase bypass.
- Prefer structured data, targeted DOM, and deterministic locators; bound retries and never loop indefinitely.
- Preserve evidence distinctions: observed, official-published, calculated, and unverified.
- Stop before personal, passport, payment, or final purchase data.

### Task 1: Establish contracts and bounded fallback orchestration

**Files:**
- Create: `flight_verifier/__init__.py`
- Create: `flight_verifier/models.py`
- Create: `flight_verifier/errors.py`
- Create: `flight_verifier/orchestrator.py`
- Test: `tests/test_orchestrator.py`

**Interfaces:**
- `FlightSearchRequest`, `FlightCandidate`, `VerificationResult`, and `EvidenceLevel` in `models.py`.
- `VerificationLayer` protocol with `name` and `verify(request, candidate) -> VerificationResult`.
- `FallbackOrchestrator(layers, max_attempts=1).verify(request, candidate)` returns a result with `attempts` and `failures` metadata.

- [ ] Write tests proving layer order, fallback after a bounded failure, success short-circuiting, and immediate stop on `HumanInterventionRequired`.
- [ ] Run `python -m unittest tests/test_orchestrator.py -v` and observe the expected initial import failure.
- [ ] Implement immutable dataclasses, explicit failure types, and a one-pass orchestrator that does not retry by default.
- [ ] Run the focused test and the full test suite.

### Task 2: Add discovery and official-source adapter boundaries

**Files:**
- Create: `flight_verifier/discovery.py`
- Create: `flight_verifier/adapters/__init__.py`
- Create: `flight_verifier/adapters/base.py`
- Create: `flight_verifier/adapters/sri_lankan.py`
- Test: `tests/test_adapters.py`

**Interfaces:**
- `DiscoveryProvider.search(request) -> list[FlightCandidate]`.
- `OfficialAirlineAdapter` implements `VerificationLayer` and exposes `airline_code`.
- `SriLankanAdapter` accepts an injected `OfficialSiteClient`; it must return a typed result or a bounded `AdapterUnavailable`/`HumanInterventionRequired` error.

- [ ] Test that a discovery provider result retains source URL, observed timestamp, and candidate fare fields.
- [ ] Test that the SriLankan adapter maps a fixture payload into refund, no-show, change, baggage, and source fields without doing network I/O.
- [ ] Implement the base adapter and a fixture-backed SriLankan mapping; leave live navigation as an injected client boundary.
- [ ] Run `python -m unittest tests/test_adapters.py -v`.

### Task 3: Document wiring, safety gates, and validation limits

**Files:**
- Create: `README.md`
- Create: `tests/fixtures/sri_lankan_biz_value.json`
- Create: `tests/test_models.py`

- [ ] Test request validation rejects missing airports/dates and verifies no purchase action exists in the public interfaces.
- [ ] Add a fixture and model tests for evidence levels, verified-at timestamps, and calculated-vs-observed refund values.
- [ ] Document the fallback sequence, adapter lifecycle, structured/network client expectations, human-intervention stop conditions, and commands for tests.
- [ ] Run the complete suite with `python -m unittest discover -s tests -v`.
- [ ] Perform a read-only Git diff/status review and report that live airline navigation remains unverified until a real client is supplied.
