"""Artifact regression fixtures only, not a resolver or functional conformance suite.

SCHEMA_CHECKS wires each manifest `schema` entry to positive/negative shape
fixtures. EXTRA_CHECKS cover draft additions whose normative tests stay todo.
"""
from copy import deepcopy

BASE = "https://4did.org/schemas/2.4/"
ID = "4did:id:6c986e8b29c144bb9c5701c8e9cf1564:Z6F5o8oBRvOS6zD4K1m2nQ"
LEGACY = "4did:h3:8928308280fffff:AZmR3kB8dH2qT7vLxN1pWg"
EXPLICIT = "4did:h3:8928308280fffff:Q3qP1zV9fT2xLmN8wK5aBg:20260503T141500Z"
NOW = "2026-11-03T12:00:00Z"
LATER = "2026-11-03T12:05:00Z"
POSE = {"position": [1, 2, 3], "orientation": [0, 0, 0, 1]}
PROVENANCE = {"producer": "external:survey", "method": "external-registration"}
REGISTRATION = {
    "frame": LEGACY, "tier": "navigational", "confidence": 0.8,
    "valid_from": NOW, "valid_to": LATER, "status": "accepted",
    "provenance": {**PROVENANCE, "registered": NOW, "evidence_refs": ["evidence:1"]},
}
STATE = {
    "id": ID, "parent": LEGACY,
    "anchor": {"variant": "h3", "cell": "8928308280fffff", "resolution": 9},
    "pose": POSE, "time": {"source": NOW, "publish": NOW, "bound_s": 0.01},
    "sequence": 1, "producer": "external:survey", "validity_s": 10,
}
DECISION = {
    "decision_id": "decision:1", "outcome": "no_acceptable_match",
    "reason": "Completed declared scope; no acceptable association.",
    "candidates": [], "evidence_refs": ["evidence:1"], "provenance": PROVENANCE,
    "authority": "authority:operator", "policy_ref": "policy:ingest",
    "scope": {"registries": ["assets"], "authorities": ["authority:operator"],
              "indexes": ["exact-identifier", "accepted-candidates"]},
    "limits": {"max_lookups": 100, "max_candidates": 20, "max_elapsed_ms": 500},
    "lookup_complete": True, "exhausted": False,
    "decided_at": NOW, "expires_at": LATER,
}


def changed(value, **updates):
    return {**deepcopy(value), **deepcopy(updates)}


def without(value, *keys):
    return {k: deepcopy(v) for k, v in value.items() if k not in keys}


def common(name):
    return BASE + "common.json#/$defs/" + name


# Each case is (schema reference, expected validity, instance).
SCHEMA_CHECKS = {
    "/conf/core/descriptor": [
        (common("fourdid"), True, EXPLICIT),
        (common("fourdid"), False, "4did:h3:8928308280fffff:short:20260503T141500Z"),
    ],
    "/conf/core/genesis-implicit": [
        (common("fourdid"), True, LEGACY),
        (common("fourdid"), True, EXPLICIT),
        (common("fourdid"), False, EXPLICIT.replace("20260503T141500Z", "not-a-time")),
    ],
    "/conf/core/uri-form": [
        (common("fourdid"), True, ID),
        (common("fourdid"), True, LEGACY.replace(":AZm", ";v=floor.12.b7:AZm")),
        (common("fourdid"), True, "4did:oct:AZmR3kB8dH2qT7vLxN1pWg.root:" + LEGACY.split(":")[-1]),
        (common("fourdid"), False, ID + ":20261103T120000Z"),
        (common("fourdid"), False, ID.replace(":Z6F", ";v=floor.1:Z6F")),
        (common("fourdid"), False, ID.replace("4did:", "http:")),
    ],
    "/conf/core/state-fields": [
        (BASE + "state.json", True, STATE),
        (BASE + "state.json", True, changed(STATE, registrations=[])),
        (BASE + "state.json", True, changed(STATE, registrations=[
            REGISTRATION, changed(REGISTRATION, frame=EXPLICIT, transform=POSE)])),
        (BASE + "state.json", False, without(STATE, "parent")),
        (BASE + "state.json", False, changed(STATE, parent=[LEGACY, EXPLICIT])),
        (BASE + "state.json", False, changed(STATE, parents=[LEGACY, EXPLICIT])),
        (BASE + "state.json", False, changed(STATE, anchor={"variant": "id", "cell": "opaque", "resolution": 0})),
        (BASE + "state.json", False, changed(STATE, registrations=[without(REGISTRATION, "status")])),
    ],
    "/conf/core/timestamps": [
        (BASE + "state.json", True, STATE),
        (BASE + "state.json", False, changed(STATE, time={"source": "yesterday", "publish": NOW})),
        (BASE + "state.json", False, changed(STATE, time={"source": NOW, "publish": NOW, "bound_s": -1})),
    ],
    "/conf/core/uncertainty": [
        (common("uncertainty"), True, {"position_cov_upper": [1, 0, 0, 1, 0, 1], "confidence": 0.8}),
        (common("uncertainty"), False, {"position_cov_upper": [1, 2, 3]}),
        (common("uncertainty"), False, {"confidence": 1.1}),
        (common("uncertainty"), False, {"orientation_sigma_rad": -1}),
    ],
    "/conf/core/provenance": [
        (common("provenance"), True, PROVENANCE),
        (common("provenance"), False, without(PROVENANCE, "producer")),
        (common("provenance"), False, changed(PROVENANCE, tier="metric", registered=NOW)),
        (common("provenance"), True, changed(PROVENANCE, tier="metric", registered=NOW, rms_m=0.01)),
        (common("registration"), True, REGISTRATION),
        (common("registration"), False, changed(REGISTRATION, provenance=PROVENANCE)),
    ],
    "/conf/core/labels": [
        (common("label"), True, {"text": "Door", "lang": "en", "source": "operator", "valid_from": NOW}),
        (common("label"), False, {"lang": "en"}),
    ],
    "/conf/core/relation": [
        (common("relation"), True, {"type": "identified_as", "registry": "asset", "external_id": "123"}),
        (common("relation"), True, {"type": "observed_by", "target": LEGACY}),
        (common("relation"), False, {"type": "identified_as"}),
        (common("relation"), False, {"type": "proxy_of"}),
    ],
    "/conf/core/represents": [
        (common("relation"), True, {"type": "represents", "target": ID, "kind": "mesh", "captured": NOW,
                                   "lod": "room", "license": "license:1", "provenance": PROVENANCE}),
        (common("relation"), False, {"type": "represents", "kind": "mesh"}),
    ],
    "/conf/motion/fields": [
        (BASE + "state.json", True, changed(STATE, ext={"motion": {"velocity": [1, 0, 0], "confidence": 0.8}})),
        (BASE + "state.json", False, changed(STATE, ext={"motion": {"velocity": [1, 0]}})),
        (BASE + "state.json", False, changed(STATE, ext={"motion": {"confidence": -0.1}})),
    ],
    "/conf/semantics/fields": [
        (BASE + "state.json", True, changed(STATE, ext={"semantics": {"class": "door", "affordances": ["openable"]}})),
        (BASE + "state.json", False, changed(STATE, ext={"semantics": {"class": 123}})),
    ],
    "/conf/semantics/localization": [
        (BASE + "state.json", True, changed(STATE, ext={"semantics": {"affordances": ["localization"], "localization_quality": 0.5}})),
        (BASE + "state.json", False, changed(STATE, ext={"semantics": {"localization_quality": 2}})),
    ],
    "/conf/lifecycle/observation-record": [
        (BASE + "observation.json", True, {"sensor_id": "sensor:1", "source": NOW, "frame": LEGACY,
            "pose": POSE, "classification": "door", "confidence": 0.8, "evidence_hash": "hash:1", "expiry": LATER,
            "candidate_4did": ID}),
        (BASE + "observation.json", False, {"sensor_id": "sensor:1", "candidate_4did": ID}),
    ],
    "/conf/domain/declaration": [
        (BASE + "domain.json", True, {"id": ID, "grid": "oct", "mode": "scenario", "extent_policy": "fixed",
            "time_mapping": {"rate": 1}, "authority": "authority:1", "derived_from": LEGACY}),
        (BASE + "domain.json", False, {"id": ID, "grid": "oct", "mode": "scenario", "extent_policy": "fixed",
            "time_mapping": {"rate": 1}, "authority": "authority:1"}),
        (BASE + "domain.json", False, {"id": ID, "grid": "id", "mode": "real", "extent_policy": "fixed",
            "time_mapping": {"rate": 1}, "authority": "authority:1"}),
    ],
}

# Deliberately not wired as full normative tests. These are additional shape
# regressions; the new genesis-privacy/reconciliation tests remain todo.
EXTRA_CHECKS = []
for field in ("frame", "tier", "confidence", "valid_from", "valid_to", "provenance", "status"):
    EXTRA_CHECKS.append((common("registration"), False, without(REGISTRATION, field)))
for updates in (
    {"parent": LEGACY}, {"frame": "not-an-id"}, {"tier": "survey-ish"},
    {"confidence": 1.1}, {"valid_to": "tomorrow"}, {"status": "verified"},
    {"transform": {"position": [1, 2], "orientation": [0, 0, 0, 1]}},
    {"transform": changed(POSE, scale=[1, 2, 3])},
    {"transform": changed(POSE, scale=0)},
    {"provenance": changed(REGISTRATION["provenance"], evidence_refs=[])},
    {"provenance": without(REGISTRATION["provenance"], "registered")},
    {"provenance": changed(REGISTRATION["provenance"], tier="logical")},
    {"provenance": changed(REGISTRATION["provenance"], method="")},
    {"tier": "metric"},
):
    EXTRA_CHECKS.append((common("registration"), False, changed(REGISTRATION, **updates)))
for updates in (
    {"tier": "logical"}, {"transform": changed(POSE, scale=0.001)},
    {"provenance": changed(REGISTRATION["provenance"], tier="navigational")},
    {"tier": "metric", "provenance": changed(REGISTRATION["provenance"], rms_m=0.01)},
    {"status": "disputed"}, {"status": "expired"},
):
    EXTRA_CHECKS.append((common("registration"), True, changed(REGISTRATION, **updates)))
for outcome in ("reuse", "no_acceptable_match", "ambiguous", "conflict", "rejected"):
    decision = changed(DECISION, outcome=outcome)
    if outcome == "reuse":
        decision["selected_id"] = ID
    EXTRA_CHECKS.append((BASE + "reconciliation.json", True, decision))
for updates in (
    {"outcome": "unknown"}, {"lookup_complete": False}, {"exhausted": True},
    {"outcome": "reuse"}, {"selected_id": ID}, {"candidates": ["bad"]},
    {"limits": {"max_lookups": 0, "max_candidates": 20, "max_elapsed_ms": 500}},
    {"expires_at": "tomorrow"}, {"evidence_refs": []},
):
    EXTRA_CHECKS.append((BASE + "reconciliation.json", False, changed(DECISION, **updates)))
for field in DECISION:
    EXTRA_CHECKS.append((BASE + "reconciliation.json", False, without(DECISION, field)))
EXTRA_CHECKS.append((BASE + "reconciliation.json", True,
                     changed(DECISION, outcome="ambiguous", lookup_complete=False, exhausted=True)))
