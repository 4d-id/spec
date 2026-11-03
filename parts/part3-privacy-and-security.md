# 4D-ID 2.4, Part 3: Privacy and security

**Unified Spatiotemporal Identity for Shared Reality. Working draft offered for community review, Part 3 of 6.**

| | |
|---|---|
| Editors | D. Lorenzini and N. Lorenzini, Quantum Studio |
| Version | 2.4 (working draft) |
| Date | November 3, 2026 |
| Status | Working draft offered for community review. Not adopted by any standards body. |

## Abstract

A pose stream with history and prediction is a surveillance system unless the draft requires otherwise, and a fabric consulted by things that move needs requirements rather than considerations. This Part specifies pseudonyms, scoped disclosure, retention, consent, and place policy, and the security class: authenticated operations, signed fabric, disclosure inheritance, erasure, audit, and, for the assured profile, policy-neutral labels and authenticated dynamic state.

## Conformance

This Part defines the requirements classes `privacy` and `security`. Conformance, profiles, normative references, terms, and conventions are in Part 1. Numbering is unique across the family (Part 1, 5.5). `security` 12.1 is required by every profile; other subclauses bind to the classes they name.

---

The non-spatial `id` mode (7.2) avoids embedding minting place or time in new identifiers. It does not replace consent, access controls, pseudonyms, or protection against linkability; legacy spatial identifiers remain valid and may retain sensitive minting metadata. Authority attribution fields are not proof; deployments select authentication and authorization mechanisms under Clause 12 and evaluate scoped grants and disputes under 14.4.

## 11. Privacy (requirements class: `privacy`)

This clause applies wherever tracked entities include humans or human-associated objects (phones, wearables, vehicles, residences). Deployments tracking only infrastructure, machinery without operators, or geographic features declare it not applicable.

> **/req/privacy/pseudonym**
> Human-associated entities SHALL carry pseudonymous local descriptors whose binding to real-world identity is held only by parties with declared dereferencing credentials. Pseudonyms SHALL be distinct per domain and per layer unless the entity's authority opts into a shared one.

> **/req/privacy/scoped-disclosure**
> A 4D-State MAY carry a disclosure policy reference; implementations SHALL resolve disclosed precision at delivery from the consumer's credentials. One identity, many precisions: a road operator sees a vehicle at meter precision, the public at block precision.

> **/req/privacy/retention**
> Every history and prediction entry SHALL carry an expiry or time-to-live. Expired entries SHALL be deleted and SHALL NOT be propagated. Expired unconfirmed predictions SHALL be discarded. Retention is enforced in wall time regardless of domain time (17.5). Attestations follow the issuer's retention policy and are kept distinct from operational history.

> **/req/privacy/consent**
> The family governs promotion and disclosure of externally produced observations and reconstructions; it does not create them. A human-associated entity SHALL NOT be proxied (17.3) into any layer or domain, and observations or reconstructions capturing a person or a surface a place policy marks private SHALL NOT be promoted to persistent entities or almanacs, without an opt-in recorded by the entity's authority. Opt-in is scoped and revocable; revocation terminates proxies and triggers erasure (12.4).

> **/req/privacy/place-policy**
> A zone authority (14.1) MAY publish a place policy; domains, layers, and propagation layers SHALL honor it. A policy MAY restrict which layers may be proxied into the zone, which affordances (9.4) proxies may carry, which activity classes a domain may host there, and the minimum disclosure resolution for human-associated entities. The policy language is not specified.

## 12. Security (requirements class: `security`)

The threat model: producers may lie; resolvers and caches may be compromised; domains may be hostile to one another; consumers may attempt to learn more than their credentials allow; the physical world is the asset being protected.

### 12.1 Baseline (required by every profile)

> **/req/security/authenticated-operations**
> Minting, acceptance/recording of externally supplied registration results, structural updates, lifecycle transitions, authority transfer, merge, and proxy rebinding SHALL be authenticated to a principal. Merge SHALL be authorized by the authorities of both identities or by the home zone and recorded in the derivation chain.

> **/req/security/replay**
> Consumers SHALL reject records whose sequence number is not greater than the last accepted for that 4D-ID, except during documented replay after disconnect (13.5).

> **/req/security/limits-and-keys**
> Minting, lease renewal, instancing, subscription, and portal creation SHALL be rate-limited per principal and per layer. Every signing key used by this family SHALL be rotatable, and every signed object SHALL identify its key.

Pose is not authenticated by the core. `velocity_violation` (13.5) flags implausible motion; `presence` (9.3) provides proof. Deployments acting on pose for access control, billing, or safety SHOULD require P4.

### 12.2 Signed fabric (required with `fabric` and `scale`)

> **/req/security/attested-delegation**
> Zone delegation (14.1) SHALL be verifiable by a signature chain from the domain root. Resolution responses, positive and negative, SHALL be signed by the responding authority with the TTL inside the signed content.

> **/req/security/signed-content**
> Almanacs (16.1) SHALL be signed by the zone authority. Portal links (17.2) SHALL be signed by the authorities of both aperture frames, and traversal SHALL default to deny. Session handle tables (16.3) SHALL be exchanged over a channel bound to the session.

### 12.3 Cross-domain flow (required with `domain`)

> **/req/security/disclosure-inheritance**
> A proxy SHALL NOT disclose pose, semantics, extents, state, rig, or motion to a consumer at finer fidelity than the source's disclosure policy permits that consumer. Following secondary references from a human-associated entity SHALL be a credentialed operation under the same policy.

> **/req/security/perception-provenance**
> An identity minted after externally supplied perception/grounding evidence and a resolve-first check (15.1) SHALL carry classification provenance (9.4). Re-identification confidence and corroboration are external evidence fields and policy inputs, not algorithms defined here. Place policy MAY require a minimum confidence or corroboration from more than one sensor before an externally evidenced entity may carry collidable, occluder, or hazardous affordances.

### 12.4 People and places (required with `privacy`)

> **/req/security/aggregate-suppression**
> In zones marked sensitive by place policy, aggregate states (16.6), density signals, and cell-split events SHALL be quantized or suppressed below a declared population threshold.

> **/req/security/erasure**
> On revocation or a documented erasure request, the entity and its proxies SHALL move to terminal and be purged from almanacs, history, digests, and instanced domains within a declared window, and the zone digest (16.5) SHALL be usable to demonstrate the purge.

### 12.5 Audit (required with `fabric`)

> **/req/security/audit**
> Each zone SHALL keep a signed, hash-chained, append-only log of candidate decisions, authorized merges, splits, structural history events, authority transfers, consent grants and revocations, erasures, place-policy changes, almanac generations, and portal creation and removal, queryable by credentialed parties within the zone's retention policy. Implementations proxying human-associated entities SHALL pass the functional tests for disclosure inheritance, consent, and erasure, not inspection alone.

### 12.6 Assured (required by P6)

The fields here are opaque to this family and interpreted only through a referenced policy. No classification scheme is defined or implied; a deployment maps its own onto them.

> **/req/security/assured-labels**
> Every 4D-State, observation, relation, and snapshot in an assured deployment SHALL carry a security label and a releasability marking, both opaque, with a policy reference that governs their interpretation; a producer authentication reference; and, where the producing device attests its own integrity, a device attestation reference. A record produced by downgrade or redaction SHALL carry redaction provenance referencing the origin record without disclosing its content.

> **/req/security/authenticated-state**
> Dynamic state in an assured deployment SHALL have authenticated provenance through an authenticated transport or a per-session integrity chain covering sequence numbers, such that insertion, replay, and modification are detectable; a signature on every record is not required. Key and device revocation status SHALL be verifiable by consumers, and records under a revoked key SHALL be flagged, not silently dropped.

---

## Annex A (normative). Tests for Part 3

| Test | Method | Purpose |
|---|---|---|
| `/conf/privacy/pseudonym` | F | Verify dereferencing requires credentials; verify distinct pseudonyms across two domains absent opt-in. |
| `/conf/privacy/scoped-disclosure` | F | Query one entity at two credential levels; verify differing precision. |
| `/conf/privacy/retention` | F | Advance past expiry, including in a paused domain; verify deletion and non-propagation. |
| `/conf/privacy/consent` | F | Proxy and reconstruct a human-associated entity without opt-in; verify refusal; revoke; verify termination. |
| `/conf/privacy/place-policy` | F | Forbid a layer in a zone; verify proxies in that layer refused there. |
| `/conf/security/authenticated-operations` | F | Attempt unauthenticated minting, transfer, and merge; verify rejection; verify merge recorded. |
| `/conf/security/replay` | F | Replay a record; verify rejection. |
| `/conf/security/limits-and-keys` | F, I | Exceed rates; verify limiting; verify key identifiers on signed objects. |
| `/conf/security/attested-delegation` | F | Present a broken delegation chain; verify refusal; verify negative responses signed. |
| `/conf/security/signed-content` | F | Present an unsigned almanac, a one-signature portal, and an unbound handle table; verify each refused. |
| `/conf/security/disclosure-inheritance` | F | Query a proxy's pose and semantics with low credentials; verify fidelity bounded by source policy; verify reference traversal refused. |
| `/conf/security/perception-provenance` | D, F | Verify provenance and policy handling for externally supplied evidence on perceived/grounded identities; verify no perception, matching, localization, or registration implementation is required and collidable is withheld below the policy floor. |
| `/conf/security/aggregate-suppression` | F | Query aggregates for a sensitive zone below threshold; verify suppression. |
| `/conf/security/erasure` | F | Revoke consent; verify purge everywhere within the window; verify digest demonstrates it. |
| `/conf/security/audit` | F | Perform candidate and authorized merge decisions plus other logged operations; verify chained signed entries; tamper; verify detection. |
| `/conf/security/assured-labels` | D, F | Validate label, releasability, policy and authentication references; downgrade a record; verify redaction provenance without origin content. |
| `/conf/security/authenticated-state` | F | Insert, replay, and modify records on the session; verify detection; revoke a key; verify flagging. |

*End of Part 3.*
