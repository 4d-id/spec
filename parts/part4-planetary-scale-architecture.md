# 4D-ID 2.3, Part 4: Planetary-scale architecture

**Unified Spatiotemporal Identity for Shared Reality. Candidate Open Standard Working Draft, Part 4 of 6.**

| | |
|---|---|
| Editors | D. Lorenzini and N. Lorenzini, Quantum Studio |
| Version | 2.3 (working draft) |
| Date | September 2026 |
| Status | Candidate open standard working draft, offered for community review. Not adopted by any standards body. |

## Abstract

How the core behaves when the hierarchy holds a planet: region-keyed propagation with backpressure and fourteen failure classes; delegated resolution with home registers and single-writer local authority; an identity lifecycle in which observations travel as evidence and identities survive handoff among external perception/grounding systems, loss of contact, and virtual sprawl; and the scale mechanisms without which implementations would not interoperate at scale. Performance techniques internal to one implementation are in Part 6.

## Conformance

This Part defines the requirements classes `propagation`, `fabric`, `lifecycle`, and `scale`. Conformance, profiles, normative references, terms, and conventions are in Part 1. Numbering is unique across the family (Part 1, 5.5). 

---

## 13. Propagation and failure handling (requirements class: `propagation`)

4D-States flow from producers (sensors, vehicles, robots, simulators, agents) to consumers (planners, fleet managers, twins, renderers, other agents). Producer count is unbounded, consumer interest is spatial rather than entity-keyed, and update rate exceeds query rate by orders of magnitude.

### 13.1 Region-keyed streaming

> **/req/propagation/region-keyed**
> Producers SHALL tag each record with the DGGS cell of its current anchor at a *declared* routing resolution. Records SHALL be delivered by cell. Consumers SHALL subscribe by cell or contiguous cell set, and SHALL be able to subscribe to the descendants of a single 4D-ID.

> **/req/propagation/interest**
> Implementations SHALL accept interest expressions at cell granularity, filtered by layer (15.5). Derived expressions (radius around a moving point, viewshed, predicted path) MAY be accepted and SHALL resolve to cell sets at evaluation time.

### 13.2 Backpressure

> **/req/propagation/priority**
> Records and subscriptions MAY carry an ordinal priority. Priority SHALL be granted by the zone authority, never self-declared by a producer, and SHALL be honored consistently by backpressure, relays, and coalescing. The levels are *declared*; a typical ordering is critical alert, nearby moving entity, routine telemetry, background reconstruction.

> **/req/propagation/backpressure**
> When a consumer cannot keep up, the propagation layer SHALL drop rather than block producers, SHALL deliver the newest record per entity per interval in priority order and discard superseded ones, and SHALL signal drops with an indicator carrying the sequence range lost. Producer-side blocking on a slow consumer is non-conformant.

### 13.3 Partition

> **/req/propagation/partition**
> On partition, each side SHALL continue operating with the records it holds and SHALL mark state from the unreachable side stale. On heal, reconciliation SHALL follow 13.5 and, where `scale` is claimed, 16.5. Availability is preferred; an implementation choosing consistency declares its model.

### 13.4 Failure classes

> **/req/propagation/failure-handling**
> Implementations SHALL handle each of the fourteen classes below as specified and SHALL document the handling in the conformance statement.

**Structural**

| Class | Required handling |
|---|---|
| `unreachable_parent` | Mark the entity unanchored; continue in the local frame; suspend upward composition; inform consumers. |
| `pose_conflict` | Two records under one 4D-ID at overlapping times disagree beyond tolerance. Surface the conflict; resolution policy is *declared*. |
| `stale_attestation` | Valid signature, expired freshness. Reject as proof; keep as history. |
| `resolution_mismatch` | Coerce per 13.6; emit a loss-of-precision indicator. |
| `hierarchy_loop` | Reject at write time; reads use depth-bounded traversal. |

**Connectivity**

| Class | Required handling |
|---|---|
| `intermittent_disconnect` | On reconnect, detect sequence gaps; replay from buffer or mark the gap and continue with degraded confidence. |
| `extended_offline` | Entity known to be operating (vehicle in a tunnel, robot in a basement, drone beyond link). Last state remains queryable as offline_active with the source-to-now gap; on reconnect, replay in order and reconcile. |
| `lossy_channel` | Treat gaps as missing data, never as state change; report measured loss rate; consumers above a *declared* threshold degrade or escalate. |
| `partition` | Per 13.3. |
| `asymmetric_reachability` | Never assume bidirectional reachability; use the channel on which a subscription was established. |
| `lost_contact` | Offline beyond the *declared* lost-threshold with no authoritative termination. Move to lost_contact; keep last state queryable with the gap; accept the entity's return through replay (13.5). Loss of communications never moves an entity to terminal. |

**Operational**

| Class | Required handling |
|---|---|
| `timestamp_drift` | Source time implausibly far from receive time. Accept; flag; never rewrite. |
| `overload` | Degrade per 13.2 and, where claimed, 16.6; never block producers. |
| `velocity_violation` | A physical-mode record inconsistent with prior pose and declared bounds, without a discontinuity marker. Accept; flag; forward with the flag. Rejection is not permitted, because the cause may be a faulty sensor, a spoofed pose, or an undeclared mode change, and authenticity reasoning needs to see it. |

### 13.5 Reconnect and replay

> **/req/propagation/replay**
> A reconnecting producer SHALL replay accumulated records in sequence order. A reconnecting consumer SHALL reconcile replayed records against any interim predictions and SHALL accept sequence numbers below its last accepted only within the documented replay.

### 13.6 Resolution coercion

Identify the coarser resolution; compute each finer record's containing cell; rewrite the anchor, preserving the LCS transform; stamp a loss-of-precision indicator carrying the original resolution; propagate with the indicator. Consumers with the original source MAY upsample.

## 14. Fabric: resolution and authority (requirements class: `fabric`)

Identity is global; state is local. Resolution follows the shape that DNS and cellular mobility management converged on: delegated authority per zone, a home register, caching resolvers, time-to-live.

### 14.1 Zones and home registers

> **/req/fabric/zone**
> A deployment SHALL partition each domain into zones at a *declared* resolution. Each zone SHALL have one authoritative resolver. Delegation to finer sub-zones SHALL be discoverable from the parent zone.

> **/req/fabric/home-register**
> The zone containing an entity's genesis anchor is its home zone and SHALL maintain the identifier of the zone currently holding the entity's state. A zone accepting an entity SHALL notify the home zone within the entity's validity window. Resolution of any 4D-ID is therefore home zone (parsed from the identifier) to current zone to state; no global index is required or assumed.

> **/req/fabric/caching**
> Resolvers SHALL cache positive and negative responses with TTLs *declared* by the authoritative zone and SHALL serve recursive resolution so consumers never contact zone authorities directly.

### 14.2 Handoff

> **/req/fabric/handoff**
> When an entity's anchor moves to a new zone, it SHALL be registered in the new zone before deregistration from the old. The old zone SHALL forward for a *declared* grace period. A vehicle crossing a city boundary, a container lifted onto a ship, and a headset walking between buildings all hand off the same way.

### 14.3 Authority

> **/req/fabric/single-writer**
> Each LCS SHALL have exactly one authority at any instant. Records for the frame from any other producer SHALL be rejected and reported as `pose_conflict`.

> **/req/fabric/local-first**
> A deployment SHALL designate local authority zones (a vehicle, a cell of a factory, a room, a session) within which the local authority is authoritative in real time. Remote and cloud components SHALL reconcile afterward and SHALL NOT be in the control loop of a local authority zone. Authority transfer SHALL emit a structural update carrying the new producer identifier and a generation increment (16.4); the election and transfer mechanism is *declared*.

## 15. Identity lifecycle (requirements class: `lifecycle`)

Perception services may produce detections by the thousand per second; virtual content is created by anyone and forgotten by everyone. These rules keep the identity space clean.

### 15.1 Observation and identity

> **/req/lifecycle/observation**
> An observation SHALL be treated as evidence only and SHALL NOT be propagated as identity state. Resolver/ingest SHALL first check exact identifiers and acceptable existing identities. External matching, grounding, re-identification, or SEGS services MAY submit candidate results, but those functions are not specified or run by this family. If an acceptable existing match exists, it SHALL be reused. Only when no acceptable match exists may an authorized resolver mint a new or provisional 4D-ID; creator-declared persistence is subject to the same check. Ambiguity SHALL produce candidate records and no automatic mint or merge. An identity minted below a *declared* confidence threshold SHALL be provisional until the threshold is crossed; its identity confidence is carried in provenance (7.8).

> **/req/lifecycle/observation-record**
> An observation exchanged as evidence SHALL carry a sensor identifier, source time and bound, pose in a stated frame, uncertainty, classification and confidence, an evidence hash, an expiry, and optionally a candidate 4D-ID supplied by an external matcher. The candidate is non-authoritative evidence and SHALL NOT change identity or state. An observation SHALL have no home register, lease, history, or relations other than `observed_by` from accepted identity state it supports, and SHALL expire without propagation.

A radar, a camera, a drone, and an operator may all produce evidence before anyone knows it is one thing. Their observations and externally supplied candidate associations travel as evidence; an identity is reused or minted only through the resolve-first lifecycle.

### 15.2 Merge and split

> **/req/lifecycle/merge**
> When an authorized resolver decision, based on externally supplied evidence, determines that two 4D-IDs denote one entity, the survivor SHALL be the earlier genesis, and the merge SHALL be authenticated (12.1). Similarity or candidate evidence alone SHALL NOT merge identities. Each other SHALL move to merged with a derivation reference to the survivor, SHALL remain resolvable through its home register within retention, and SHALL redirect. Entities in different domains SHALL NOT be merged (17.6).

> **/req/lifecycle/split**
> When an authorized resolver decision, based on externally supplied evidence, determines that one 4D-ID denotes several entities, new identities MAY be minted with derivation references to the original, whose continuation or termination SHALL be recorded in the derivation. Candidate evidence alone SHALL NOT split or mint identities.

### 15.3 Leases and layers

> **/req/lifecycle/lease**
> Every virtual entity SHALL carry a lease; physical entities MAY. An unrenewed entity SHALL move to terminal at expiry without producer involvement. Renewal is a state record.

> **/req/lifecycle/layer**
> Every entity SHALL declare a layer (public, an application, a private session). Subscriptions filter by layer; entities in different layers SHALL NOT be reported as `pose_conflict` for sharing a pose. Two applications may each attach content to the same shelf; a planning session and a public tour may share a building.

## 16. Scale (requirements class: `scale`)

The mechanisms here are those whose absence would prevent two implementations from interoperating at scale. Techniques internal to one implementation are in Part 6.

### 16.1 Almanac and ephemeris

> **/req/scale/almanac**
> Each zone SHALL publish a cell almanac: a content-addressed, immutable, signed snapshot of its static-mode entities, identified by hash and zone generation. Static entities SHALL be distributed by almanac and SHALL NOT appear on the live stream except as structural updates producing a new almanac. The live stream SHALL carry only physical and teleportable entities, structural updates, lifecycle transitions, and lease renewals.

This is the split the automated-driving community knows as the permanent versus dynamic layers of the Local Dynamic Map, and satellite navigation as almanac versus ephemeris. A vehicle bootstraps its route from cache and subscribes only to what moves.

### 16.2 Publishing

> **/req/scale/threshold-publish**
> A physical-mode producer SHALL declare an error budget (position, orientation). Between keyframes it SHALL publish only when observed pose diverges from the model-predicted pose beyond the budget, or when decayed confidence (9.1) falls below a *declared* floor. Consumers SHALL treat absence of records within the validity window as "prediction holds."

> **/req/scale/keyframe-delta**
> Implementations SHALL support keyframes (full 4D-State) and deltas (handle, sequence, source time, pose offset from the last keyframe, changed extension fields). Keyframes SHALL be emitted on structural change, discontinuity, mode or lifecycle transition, and at a *declared* maximum interval. A consumer lacking the referenced keyframe SHALL request it and SHALL NOT apply the delta.

> **/req/scale/change-locality**
> A descendant SHALL NOT republish when only its parent moved. Consumers derive descendant global poses by composition (7.6). A ship carrying ten thousand containers is one record; a bus carrying fifty passengers is one record.

### 16.3 Session handles

> **/req/scale/handle-table**
> Within a propagation session, records SHALL reference entities by a 32-bit session-scoped handle. The handle table SHALL be exchanged at subscription, updated incrementally, and never persisted or reused across sessions.

### 16.4 Generations and digests

> **/req/scale/generation**
> Every node SHALL carry a monotonic generation counter incremented on any transform or parent change. A cached composed transform SHALL record the generation of each ancestor it composed from; validity is a comparison against current generations.

> **/req/scale/digest**
> Each zone SHALL maintain a digest over its (4D-ID, sequence, generation) triples, structured for independent sub-range comparison (Merkle tree or equivalent) and rooted at the zone generation. On reconnect and partition heal, peers SHALL reconcile by digest and exchange only differing entries.

### 16.5 List then watch, and snapshots

> **/req/scale/list-then-watch**
> The consumer protocol for a zone SHALL be: fetch the almanac and current dynamic state at generation N, then subscribe to changes after N. The propagation layer SHALL maintain a compacted last-value view per entity so a list at any generation returns current state.

> **/req/scale/snapshot**
> A snapshot SHALL name one coherent picture across zones: a vector of (zone, generation) pairs, a reference time, a maximum permitted skew between zones, and a staleness bound. Implementations SHALL be able to serve list-then-watch at a snapshot and to report whether a given record is inside or outside it. Global consistency is not required; bounded, explicit consistency is.

An operations floor, a remote participant, two game engines, a wall display, and an AI agent asking for "picture S at time T" are looking at the same version of reality, and know it.

### 16.6 Aggregates

> **/req/scale/aggregate**
> An LCS with children MAY publish an aggregate state (centroid pose, bounding extent, child count, maximum child speed) for its subtree, marked as an aggregate, with its own sequence and generation. Consumers MAY subscribe to aggregates in place of children and SHALL drill in at a *declared* distance or angular-size threshold. When a zone applies uniform rate reduction under overload, the factor SHALL be carried in the aggregate so consumers rescale extrapolation.

A yard of containers is one record to a drone at a kilometer and thousands to a straddle carrier among them.

---

## Annex A (normative). Tests for Part 4

| Test | Method | Purpose |
|---|---|---|
| `/conf/propagation/region-keyed` | F | Verify cell tagging at routing resolution; verify cell-set and subtree subscription. |
| `/conf/propagation/interest` | F | Verify cell-granularity interest with layer filtering; verify derived expressions resolve to cells. |
| `/conf/propagation/priority` | F | Producer self-declares priority; verify ignored; authority grants it; verify honored under backpressure and by relays. |
| `/conf/propagation/backpressure` | F | Stall a consumer; verify producers unblocked, newest-per-entity delivery in priority order, drop indicator. |
| `/conf/propagation/partition` | F | Partition; verify continued operation and staleness marking; heal; verify reconciliation. |
| `/conf/propagation/failure-handling` | I, F | For each of fourteen classes, inject and verify documented handling. |
| `/conf/propagation/replay` | F | Disconnect a producer; reconnect; verify ordered replay and reconciliation. |
| `/conf/fabric/zone` | I, F | Verify zone resolution and discoverable delegation. |
| `/conf/fabric/home-register` | F | Move an entity across three zones; verify home register updated within the validity window; verify two-hop resolution. |
| `/conf/fabric/caching` | F | Resolve repeatedly; verify authority contacted once per TTL; verify negative caching. |
| `/conf/fabric/handoff` | F | Cross a zone boundary mid-stream; verify no loss and forwarding during grace. |
| `/conf/fabric/single-writer` | F | Submit for one LCS from two producers; verify second rejected as `pose_conflict`. |
| `/conf/fabric/local-first` | F | Sever the wide-area link; verify local zone continues at full rate; remove the authority; verify transfer with structural update. |
| `/conf/lifecycle/observation` | F | Inject externally produced observations and candidate evidence for one object from three sources; verify evidence-only handling, existing-identity reuse, ambiguity without automatic mint/merge, and provisional status below threshold. |
| `/conf/lifecycle/observation-record` | D, F | Validate evidence fields and optional externally supplied candidate 4D-ID; verify expiry without propagation and no home register or lease. |
| `/conf/lifecycle/merge` | F | Submit externally supplied evidence and an authorized resolver decision; verify survivor, redirect, and rejection of new records to the merged identity; verify similarity/candidates alone do not merge; attempt cross-domain merge; verify refusal. |
| `/conf/lifecycle/split` | F | Split; verify derivation references. |
| `/conf/lifecycle/lease` | F | Withhold renewal; verify terminal at expiry without producer action. |
| `/conf/lifecycle/layer` | F | Two entities at one pose in two layers; verify no conflict and layer filtering. |
| `/conf/scale/almanac` | D, F | Verify static entities in a signed almanac and absent from the live stream. |
| `/conf/scale/threshold-publish` | F | Smooth path; verify no records inside budget and one on divergence. |
| `/conf/scale/keyframe-delta` | F | Verify reconstruction from keyframe and deltas; verify a delta without keyframe refused. |
| `/conf/scale/change-locality` | F | Move a parent; verify no descendant records. |
| `/conf/scale/handle-table` | D | Verify handles, table exchange, no reuse across sessions. |
| `/conf/scale/generation` | F | Change an ancestor; verify cache detects mismatch on next read. |
| `/conf/scale/digest` | F | Partition, change 1%, heal; verify exchanged set proportional to change. |
| `/conf/scale/list-then-watch` | F | List at N, watch, compare to a fresh list; verify equivalence. |
| `/conf/scale/snapshot` | F | Serve two consumers the same snapshot; verify identical pictures; verify a later record reported outside it. |
| `/conf/scale/aggregate` | F | Subscribe at aggregate level; approach; verify drill-in; verify rate factor carried. |

*End of Part 4.*
