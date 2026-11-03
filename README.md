# 4D-ID™ Specification

**A persistent identifier for a resolved referent across systems and time.** A working draft offered for community review.

[![License: OGC / Apache-2.0](https://img.shields.io/badge/license-open-blue.svg)](#license)
[![Status: Working draft offered for community review](https://img.shields.io/badge/status-working%20draft-blue.svg)](#status)
[![Try it live](https://img.shields.io/badge/try-4d--id.org-4dd0c4.svg)](https://4d-id.org/)

4D-ID gives each resolved object, surface, agent, and environment, physical or virtual, one persistent identity that can survive movement, re-observation, vendor boundaries, and the boundary between real and virtual. It is an identity and continuity layer over the standards the world already uses (OGC GeoPose and DGGS, ISO 8601, OpenXR, glTF), not a new coordinate system.

Grounding determines which thing a record refers to; localization determines where it is. 4D-ID preserves the resolved referent across systems and time and records externally supplied state/evidence; it does not perform perception, grounding/matching or re-identification (including SEGS), localization, registration, or rendering.

The web gave every document a name that worked across every browser and server. 4D-ID does the same for the physical world.

> **Identities are shared and global, but what you can see and say about them is yours.**

## Boundaries and the 2.4 model

**OBSERVE -> GROUND -> IDENTIFY -> RESOLVE -> INTEROPERATE.** Observations are evidence; external grounding determines the referent and localization determines where; 4D-ID preserves which. SEGS is adjacent, not an in-family matcher. An acceptable existing identity is reused before any authorized mint.

An entity has one composition parent and may carry many externally supplied registration records. Registrations neither add parents nor establish identity. DGGS routes, partitions, and filters; it is not the name. New `id`-variant identifiers use opaque, non-spatial home tokens and random descriptors without embedded place, person, or time. Legacy spatial IDs stay valid as mint/routing metadata; current anchors and accepted registrations determine location. The larger identifier/grid decision remains open for 2.5.

## This repository

This is the **specification**: a versioned working draft offered for community review and possible future submission. Potential liaison targets include an OGC Standards Working Group and Khronos for the OpenXR and glTF bindings; this repository makes no adoption claim.

| Path | What it is |
|---|---|
| [`parts/`](parts/) | The specification, in six parts. Part 1 (Core) stands alone. |
| [`schemas/`](schemas/) | Partial JSON Schema 2020-12 record bindings. |
| [`encoding/2.4.md`](encoding/2.4.md) | Versioned binding status, migration, and coverage limits. |
| [`openapi/`](openapi/) | OpenAPI 3.1 description of the access operations (Clause 10). |
| [`conformance/`](conformance/) | The conformance manifest: every test this working draft defines. |
| [`CHANGELOG.md`](CHANGELOG.md) | Notable changes per version. |
| [`GOVERNANCE.md`](GOVERNANCE.md) | How this working draft is governed and possible future liaison paths. |

The **reference implementation** (a resolver you can run in an afternoon), the **SDKs**, and the **conformance CLI** live in sibling repositories:

- [`reference-resolver`](https://github.com/4d-id/reference-resolver) — the resolver, Apache-2.0
- [`js-sdk`](https://github.com/4d-id/js-sdk) — the TypeScript / JavaScript client
- [`demos`](https://github.com/4d-id/demos) — interactive browser demos, also live at [4d-id.org](https://4d-id.org/)

## Read it

Start with **[Part 1: Core](parts/part1-core.md)**. It is about thirteen pages and defines the whole model on four concepts: identity, hierarchy, pose, time. Every later part is optional.

| Part | Read it if you |
|---|---|
| [1 Core](parts/part1-core.md) | implement anything; it stands alone |
| [2 Extensions and access](parts/part2-extensions-and-queries.md) | carry motion, history, attestation, or semantics; serve queries or agents |
| [3 Privacy and security](parts/part3-privacy-and-security.md) | track people, resolve across zones, or serve static content |
| [4 Planetary-scale architecture](parts/part4-planetary-scale-architecture.md) | run more than one zone or authority, or operate identity lifecycle and externally supplied evidence/candidate matches |
| [5 Domains and presentation](parts/part5-domains-and-presentation.md) | connect simulation or generated environments to the real world |
| [6 Implementation guide](parts/part6-implementation-guide.md) | build one, and want to know which technique makes each rule cheap |

## The one rule of what is normative

A requirement is in this working draft only if two independent implementations would fail to interoperate without it. Exactly 112 normative requirements survive that rule, each linked to an Annex A test and manifest entry. Defined tests are not claims of passing implementations. Everything else is guidance in Part 6.

## Try it before you read it

External clients and demos—including an interactive resolver, an address-to-identity globe, and animated robot, drone, and ship examples—run at **[4d-id.org](https://4d-id.org/)**. The resolver may resolve and record externally supplied candidates and authorized lifecycle decisions; it does not perceive, localize, match, register, or render.

## Status

**Version 2.4, November 3, 2026: working draft offered for community review.** No standards body has adopted this draft. See [GOVERNANCE.md](GOVERNANCE.md) for possible future paths.

## Validate the artifacts

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r conformance/requirements.txt
.venv/bin/python conformance/validate.py
```

Validation checks schema and OpenAPI validity, local/versioned references, positive and negative JSON fixtures, and exact one-to-one linkage among 112 requirements, Annex A tests, and manifest entries. Wired schema checks are partial, not functional conformance; see [encoding/2.4.md](encoding/2.4.md).

## Contributing

Review the draft and open an issue or a change request. See [CONTRIBUTING.md](CONTRIBUTING.md). The specification evolves through documented, reviewable change.

## License

The specification text is offered under an open documentation license for community review. The reference implementation, SDKs, schemas, and conformance suite are licensed **Apache-2.0**. See [LICENSE](LICENSE).

The identifier format is permissionless to generate, but conforming resolution follows existing-identity-first: resolve an acceptable existing identity before minting; mint only after a completed, bounded, scoped and unexpired no-acceptable-match decision, subject to the lifecycle and authority rules. Incomplete or exhausted lookup is not no-match. This working draft is designed for royalty-free publication and implementation.
