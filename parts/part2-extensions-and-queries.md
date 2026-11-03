# 4D-ID 2.4, Part 2: Extensions and queries

**Unified Spatiotemporal Identity for Shared Reality. Working draft offered for community review, Part 2 of 6.**

| | |
|---|---|
| Editors | D. Lorenzini and N. Lorenzini, Quantum Studio |
| Version | 2.4 (working draft) |
| Date | November 3, 2026 |
| Status | Working draft offered for community review. Not adopted by any standards body. |

## Abstract

Optional extensions that ride on a 4D-State (motion, history and prediction, verifiable presence, semantics); the access operations that every client, agent, and binding calls, defined once as semantics so any transport can carry them; the query primitives; a bounded context envelope for agents; and the canonical spatial feature vector. A static twin needs none of them; a vehicle fleet needs most.

## Conformance

This Part defines the requirements classes `motion`, `history`, `presence`, `semantics`, `query`, and `features`. Conformance, profiles, normative references, terms, and conventions are in Part 1. Numbering is unique across the family (Part 1, 5.5). 

---

## 9. Extensions

### 9.1 Motion (requirements class: `motion`)

> **/req/motion/fields**
> The motion extension SHALL carry linear velocity (m/s) in the parent frame and MAY carry angular velocity (rad/s) and linear acceleration (m/s²), each sampled at source time, with a confidence in [0, 1]. It is normative for physical mode, normative between discontinuities for teleportable mode, and carries no meaning for static mode.

> **/req/motion/decay**
> A consumer extrapolating from source time to a later instant SHALL apply a declared, monotonically non-increasing decay to confidence as a function of elapsed interval and SHALL expose the decayed value with the extrapolated pose.

A trajectory planner, a render loop, and a fleet dashboard each extrapolate over different horizons; decayed confidence is what lets each decide when a prediction is no longer worth acting on.

### 9.2 History and prediction (requirements class: `history`)

> **/req/history/fields**
> The extension SHALL carry a bounded window of prior poses with source times; a bounded window of predicted poses with target times; a confidence per prediction; the predictor's model identifier and version; and retention metadata per entry (11.3).

> **/req/history/advisory**
> Predictions SHALL be marked as predictions. Consumers SHALL treat them as estimates. Predictions generated at read time and stored predictions SHALL be indistinguishable through the data interface.

The generating model is not specified. A vehicle's motion planner, a warehouse scheduler, and a learned world model all publish through the same fields.

### 9.3 Verifiable presence (requirements class: `presence`)

For drone corridors and remote identification, chain of custody in logistics, provenance of training captures, and event verification.

> **/req/presence/attestation**
> An attestation SHALL bind, under a signature from a known identity, the 4D-ID, pose, source time, producer identifier, and sequence number, and SHALL identify the hash and signature algorithms and the signing key. It SHALL declare a freshness window; older attestations SHALL be rejected as proof and preserved as history.

> **/req/presence/credential**
> Attestations SHALL be expressible as W3C Verifiable Credentials 2.0 with a defined credential type. Anchoring to a ledger is a deployment choice and SHALL NOT be required.

### 9.4 Semantics (requirements class: `semantics`)

Views (17.4), place policy (11.5), planners, and AI reasoning need to know what a thing is and what it permits. Appearance is out of scope.

> **/req/semantics/fields**
> The extension SHALL carry a class identifier from a declared namespaced taxonomy; classification provenance (model, version, confidence); affordance flags from at least {collidable, walkable, sittable, graspable, occluder, openable, hazardous, structural, immovable, localization}; and a bounding hull in the local frame. It MAY carry a discrete state from the taxonomy, and, where the `localization` affordance is set, a localization-quality value in [0, 1] advertising the quality of this feature as input to an external localizer. The hull SHALL be the authoritative geometry for affordance decisions. The taxonomy SHALL reserve namespaces for relation types (7.9), event classes, and the built environment (parcel, building, floor, unit, room, facade, window, door, riser, fixture).

> **/req/semantics/localization**
> A feature marked with the `localization` affordance is declared stable enough for an external localization service to consume as an input. A client or external localizer SHOULD prefer features with this affordance and higher localization quality and SHOULD ignore transient or seasonal features that lack it. This family neither performs matching nor localization; the quality is an advertised input-quality value.

> **/req/semantics/event**
> An event (an alert, incident, operation, or an explicitly promoted detection event) SHALL be modeled as an entity: its pose and hull give its spatial extent, its validity window gives its time interval, its class comes from the event namespace, and its subjects and supporting observations are relations. A detection remains an observation/evidence item unless deliberately promoted as an event; an event entity SHALL NOT become an identity for its detected subject. Subject identity comes from resolver decisions. No separate event record is defined; the cell-time query (10.1) answers "what happened here in this interval."

## 10. Access and queries (requirements class: `query`)

### 10.1 Access operations

A client that holds a 4D-ID needs a small, fixed set of operations whose meaning does not depend on transport. Each operation is defined by its inputs, outputs, and errors; REST, gRPC, MCP, ROS services, engine plugins, and any future protocol are bindings (Part 1, Annex B). One semantic API, many bindings.

> **/req/query/operations**
> An implementation SHALL provide the following operations with the stated semantics, over at least one documented binding:
> - `resolve(registry, external_id)` or `resolve(4did)`: the accepted existing 4D-ID and its current locator (14.1), or a signed, scoped and expiring negative only for completed lookup. Responses SHALL distinguish the five outcomes of 7.10 and retain the bounded decision metadata; incomplete or exhausted lookup is not a no-match. Resolve SHALL NOT silently mint, perceive, localize, match, re-identify/SEGS, or register; external candidate evidence is handled by lifecycle-specific services and policy.
> - `get_entity(4did)`: stable metadata (parent, motion mode, status, labels, layer, lease, semantics, relation summary).
> - `get_state(4did, at?)`: the current 4D-State, or the state at a past instant within retention where `history` is claimed.
> - `get_relations(4did, type?, direction?, at?, min_confidence?, depth?)`: relations (7.9) with validity, confidence, and provenance.
> - `query(cells, interval?, layer?, class?)`: entities by cell and time (10.2).
> - `query_events(subject?, cells?, interval, class?, min_confidence?)`: event entities (9.4).
> - `transform(from_4did, to_4did, at?)`: the composed transform and its uncertainty (7.6, 7.8).
> - `get_representations(4did, purpose, credentials)`: representations (7.9) ranked for a declared downstream consumer purpose (rendering by a client, measurement, localization input for an external localizer, agent context, remote viewing) subject to credentials, license, tier, and validity. The resolver only ranks/returns representations and metadata.
> - `get_snapshot()`: a snapshot (16.5); `list(cells, snapshot)`: state at that snapshot.
> - `watch(cells | 4did, since)`: changes after a generation or snapshot (16.5), with drop indicators (13.2).
> - `context(4did, fields?, max_entities?, max_bytes?, snapshot?)`: a context envelope (10.6).
> Operations SHALL be idempotent except `watch`, SHALL carry the snapshot or generation they answered from, and SHALL fail with a documented error rather than a partial silent result.

Agent and tool protocols carry these operations; they do not carry the high-rate 4D-State stream (13), which remains the path for robots, headsets, vehicles, and renderer clients. Ray, visibility, and context operations are data/query services; they do not render, perform visual perception, or localize.

### 10.2 Hierarchical and temporal

> **/req/query/cell-time**
> Implementations SHALL answer: all entities whose current anchor lies in a given cell or contiguous cell set at a given instant or interval; the direct children and bounded-depth descendants of a 4D-ID; and, where `history` is claimed, the pose of a 4D-ID at a past instant within retention and its derivation and structural history.

### 10.3 Relations and events

> **/req/query/relations**
> `get_relations` SHALL support filtering by type, direction, time, and minimum confidence, and bounded traversal to a declared depth, so that "what observed this entity" and "what does this entity represent" are single calls.

> **/req/query/events**
> `query_events` SHALL support filtering by subject, area, interval, class, and minimum confidence, so that "what happened near here in this interval" and "what changed in this entity" are single calls.

### 10.4 Ray-cast

> **/req/query/ray**
> A ray-cast SHALL accept a ray as (global origin, direction) or (origin 4D-ID, direction in local axes), and MAY accept maximum range, maximum hit count, a recursion policy (outermost or finest hit), and a portal policy (17.2). It SHALL return hits ordered by distance, each with the hit 4D-ID, the intersection point in the hit entity's frame, the entity's provenance, and a combined uncertainty from ray origin and entity geometry.

### 10.5 Visibility

> **/req/query/visibility**
> A visibility query SHALL accept a viewpoint pose, field-of-view parameters, and a predicted display time, and MAY accept maximum range, a layer set, an occlusion flag, and a portal policy. It SHALL return entities ordered by distance, each with a level-of-detail hint from angular size and an occlusion state (visible, partial, culled), with poses extrapolated to the display time and decayed confidence (9.1). Frustum and distance culling SHALL be supported; occlusion, where supported, SHALL use hulls, not points. The maximum sustainable rate and entity bound at that rate are *declared*.

### 10.6 Context envelope

An agent asking about a door should not receive a point cloud or a transform graph. It should receive a small, deterministic description it can reason over.

> **/req/query/context-envelope**
> `context` SHALL return, for the requested entity and within the declared `max_entities` and `max_bytes`, a field-selectable envelope containing: the 4D-ID; class and labels; parent; current pose and `as_of`; the snapshot answered from; confidence and uncertainty; affordances and hull; the highest-confidence relations by type; representation references with tier and license; provenance including any agent-run provenance; freshness; and the disclosure and license constraints that apply to the requester. The envelope SHALL contain only fields the requester's credentials permit, SHALL be deterministic for a given snapshot and request, and SHALL carry no geometry beyond hulls.

### 10.4 Canonical spatial feature vector (requirements class: `features`)

This is a hand-defined feature vector for indexing and similarity search, not a learned embedding. Learned embeddings are model-specific and are carried separately (Part 6, G.9).

> **/req/features/vector**
> P5 implementations SHALL emit, on request, a 32-element binary32 vector in the following order and SHALL NOT reorder or repurpose fields. Learned embeddings SHALL NOT be concatenated into it.

| Index | Field |
|---|---|
| 0 to 2 | Position in parent LCS (m) |
| 3 to 6 | Orientation quaternion (x, y, z, w) |
| 7 to 9 | Linear velocity (m/s), zero if static |
| 10 to 12 | Angular velocity (rad/s) |
| 13 to 15 | Linear acceleration (m/s²) |
| 16, 17 | sin, cos of UTC time of day |
| 18, 19 | sin, cos of day of year |
| 20 | Pose confidence |
| 21 | Registration RMS (m) |
| 22 to 24 | Bounding half-extents (m) |
| 25 to 27 | Motion mode one-hot (static, physical, teleportable) |
| 28 | min(depth, 12) / 12 |
| 29 | log10 of anchor cell edge length, clamped to [−3, 7], scaled to [0, 1] |
| 30, 31 | Reserved, zero |

Position is LCS-relative so that similarity search is not dominated by global magnitude; global context comes from filtering by cell first. An external indexing or matching service MAY use this vector. Similarity is not identity: externally produced matches are candidate evidence that the resolver records with provenance and decision status, not an automatic merge or mint decision.

---

## Annex A (normative). Tests for Part 2

| Test | Method | Purpose |
|---|---|---|
| `/conf/motion/fields` | D | Validate fields and mode semantics. |
| `/conf/motion/decay` | I, F | Verify declared decay; verify monotone non-increase. |
| `/conf/history/fields` | D | Validate windows, confidences, model identifier, retention metadata. |
| `/conf/history/advisory` | F | Verify prediction flag; verify ephemeral and stored predictions indistinguishable. |
| `/conf/presence/attestation` | D, F | Verify binding, algorithms, key identifier; present an expired attestation; verify rejection as proof and retention as history. |
| `/conf/presence/credential` | D | Validate as a VC 2.0 credential. |
| `/conf/semantics/fields` | D | Validate class, provenance, affordances, hull. |
| `/conf/query/operations` | F | Exercise every operation over a documented binding; verify existing-ID and signed-negative responses, no implicit minting, semantics, idempotence, snapshot tagging, and documented errors. |
| `/conf/query/cell-time` | F | Query a cell at an instant and a subtree; verify completeness; query a past pose where `history` is claimed. |
| `/conf/query/relations` | F | Query relations by type, direction, time, confidence, and depth; verify filtering and bounded traversal. |
| `/conf/query/events` | F | Query events by subject, area, interval, class; verify results and confidence filtering. |
| `/conf/query/context-envelope` | F | Request an envelope with field selection and bounds; verify determinism at a snapshot, credential filtering, size bound, and absence of geometry. |
| `/conf/query/ray` | F | Select data for rays at known geometry; verify ordered hits, local intersection data, provenance, and uncertainty without requiring rendering or visual perception. |
| `/conf/query/visibility` | F | Select data for a known frustum 30 ms ahead; verify culling, LOD hints, extrapolation, and decayed confidence without requiring rendering or localization. |
| `/conf/features/vector` | D | Validate length, order, normalization. |
| `/conf/semantics/localization` | D | Validate metadata-only localization affordance and quality on stable features as input to an external localizer; verify no localization algorithm is required and transient features lack the affordance. |
| `/conf/semantics/event` | F | Publish an event entity; verify cell-time query over its interval returns it with subjects as relations. |

*End of Part 2.*
