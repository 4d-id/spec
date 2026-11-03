# Changelog

All notable changes to the 4D-ID specification are recorded here. The specification version is independent of any implementation version.

## 2.4 - November 3, 2026 (working draft offered for community review)
- Grounding determines the referent; localization determines where; 4D-ID preserves which resolved referent continues. Preserve OBSERVE -> GROUND -> IDENTIFY -> RESOLVE -> INTEROPERATE, evidence-only observations, adjacent SEGS, and existing identity before mint.
- One composition parent plus many externally supplied registrations with frame, optional transform, tier, confidence, validity, provenance, and status. Registrations do not add parents or establish identity; strengthened strict-tree, state, and provenance requirements and tests.
- Added non-spatial `id` home-token mode within the existing grammar, with UUIDv4/entropy descriptors and no vertical reference or genesis timestamp. Legacy spatial IDs remain valid mint/routing metadata; current anchors and registrations determine location. Documented migration and left the larger identifier/grid decision open for 2.5.
- Added bounded reconciliation decisions with five explicit outcomes, evidence, authority attribution, limits, and expiry. Incomplete or exhausted lookup is not no-match; candidate records do not mutate identity or state.
- Added Part 4, 14.4: conferred authority, overlapping authority, and disputes. Authority fields are attribution, not proof; deployments retain authentication/authorization policy under Clause 12.
- Exactly 112 normative tests: retained the existing 107 and added `/conf/core/genesis-privacy`, `/conf/core/reconciliation`, `/conf/fabric/conferred-authority`, `/conf/fabric/overlapping-authority`, and `/conf/fabric/dispute`. All five new entries are `todo`; artifact/shape validation is not a functional pass claim.
- Versioned all six part headers, schema IDs/references, manifest, OpenAPI, and the new encoding pointer to 2.4. Added validation for schema/OpenAPI parsing, reference integrity, positive/negative fixtures, and exact requirement/test/manifest linkage. Preserved historical 2.3 text and existing clause numbers.
- Maturity wording is working draft offered for community review; no standards-body adoption is claimed. Technical candidate-match and candidate-record language remains.

## 2.3 — September 2026 (working draft)
- Clause 10 defined as access operations: one semantic API, many bindings (REST, MCP, and others). Added relation and event queries, purpose-based representation negotiation, snapshot access, watch, and a bounded context envelope.
- P5 (AI-Integrated) now requires `semantics`.
- Added human-readable labels (non-identity) and the promotion rule (automation proposes, authority promotes).
- Added agent-run provenance.
- Bindings annex covers OpenXR, glTF, MCP, and agent-to-agent delegation (all informative).
- Editorial: family map, scope pointers, and feature-vector depth field corrected.

## 2.2
- `localization` affordance and quality; registration tier on exterior representations; overlay-confidence rule for AR. These are affordance/quality and provenance metadata consumed by external localizers or clients, not functions performed by 4D-ID.

## 2.1
- `presentation` class: viewpoints, level-of-detail ladder, transition hints, continuity anchors, registration tier.

## 1.9
- `represents` and `identified_as` relations; vertical reference grammar and floor frames; domain mode.

## 1.8
- Identity continuity principle and structural history; `lost_contact` status; observations as ephemeral evidence; fused-state provenance; typed relations; events as entities; coherent snapshots; assured security subclause; P6 Assured profile. Observations and registration/localization values remain recorded evidence/metadata, not in-family processing.

## 1.7
- Restructured into six parts governed by the one-rule test; reduced to the requirements that carry interoperability.

## 1.1 — May 2026
- Initial working draft.
