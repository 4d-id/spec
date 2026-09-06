# 4D-ID 2.3, Part 6: Implementation guide

**Unified Spatiotemporal Identity for Shared Reality. Informative Candidate Open Standard Working Draft, Part 6 of 6.**

| | |
|---|---|
| Editors | D. Lorenzini and N. Lorenzini, Quantum Studio |
| Version | 2.3 (working draft) |
| Date | September 2026 |
| Status | Informative candidate working draft. Nothing in this Part is required for conformance. |

## G.1 Purpose

Parts 1 to 5 carry only requirements without which two implementations would not interoperate. Everything an implementer needs beyond that, and everything earlier drafts specified as SHALL but which turned out to be engineering rather than interoperability, is here. Each section names the requirement it supports and the technique that makes it cheap.

## G.2 Composition and validity (supports 7.6, 16.4)

- Cache composed transforms only through static ancestors; below a moving ancestor, hold the partial composition and multiply by the ancestor's current pose at read time. A moving ship then invalidates nothing beneath it.
- Validity check is a comparison of at most twelve generation integers. Do not build push invalidation; generation compare is cheaper and cannot fan out.
- For depth-limited local queries, compose lazily in the query kernel instead of reading cached globals; both paths must agree within declared uncertainty.

## G.3 Publishing (supports 16.2, 16.3)

- Schedule periodic keyframes at a phase derived from the entity handle so refresh load is uniform across the interval.
- Batch producers in one LCS on a shared tick with delta-encoded timestamps and a shared header. A room of thirty sensors, or a vehicle's dozen, becomes one packet per tick.
- Encode deltas against the last keyframe the consumer acknowledged, as video codecs and game netcode do.
- Within an LCS of known extent, 16-bit fixed-point positions give millimeter precision over 65 m; smallest-three quaternion packing gives 32-bit orientation. A hot pose drops from 56 bytes to 10. These belong to the Encoding Standard.
- Keep a fixed-width hot record (pose, velocity, sequence, source time, confidence, flags, at most 128 bytes) separate from cold metadata (provenance, extensions, references) reached by handle.

## G.4 Fan-out (supports 13.2, 16.6)

- Allocate delivery under a bandwidth budget by an accumulating score per entity (authority-granted priority first, then angular size at the consumer, speed, decayed confidence), reset on delivery. Random sampling degrades the foreground as fast as the background; priority accumulation keeps what matters fresh.
- When a zone saturates, reduce the accepted publish rate uniformly (time dilation) and carry the factor in the aggregate, rather than dropping producers selectively. A saturated stadium, port, or highway interchange stays coherent for everyone.
- Split a zone at the next finer resolution when producer count or rate exceeds a threshold, without interrupting subscriptions, and split ahead of forecast load (event schedules, commute patterns, shift changes).
- Serve zones with large subscriber counts through a tree of relays, each holding the compacted last-value view.
- Tag producers within a halo distance of a zone boundary (or a portal aperture) for delivery to both sides, so consumers never double-subscribe adjacent zones.
- Pre-subscribe a moving consumer to zones its velocity vector will enter within its validity window; release exited zones after a hysteresis interval; register in the new zone before leaving the old (make-before-break).
- Push visibility and derived-interest evaluation into the propagation layer so a million consumers in one district do not each cull the same million entities.

## G.5 Consumption (supports 10.3)

- Keep a structure-of-arrays layout per zone so current state uploads as one contiguous buffer, and derive the feature vector by strided access.
- Return visibility results as a GPU buffer suitable for indirect draw; avoid a host round trip per frame.
- Present remote entities from an interpolation buffer 50 to 100 ms behind source time and the consumer's own entity in the present; expose the delay so interaction logic compensates.
- Sample pose as late as possible before presentation, extrapolated to predicted display time with decayed confidence.
- Bind themed assets only to active, not provisional, sources, and do not swap assets while the source stays active unless its class changes.

## G.6 Local exchange (supports 14.3)

- Co-located producers and consumers (a vehicle platoon, robots on one floor, headsets in one room) should exchange state directly over local links (Wi-Fi Aware, UWB, sidelink, Bluetooth) with a duty cycle that falls as density rises, routing through the wide area only for state beyond local range. This is both faster and the only pattern that survives a dense zone, as the saturation of shared aircraft-broadcast channels over busy airspace demonstrates.
- Nested local authority (a robot inside a vehicle inside a port) resolves to the innermost zone for the shared child frame; election among peers should be documented and tested for the case where the elected device disappears.

## G.7 Storage (supports 9.2, 16.4)

- Key indexes by (cell prefix in the grid's hierarchical bit order, time bucket) so region queries are contiguous range scans and multi-resolution indexing is prefix length.
- Store history in fixed-duration, append-only buckets; seal, content-address, and compact with age (full poses for the last hour, keyframes for the last day, trajectory splines beyond); enforce retention by dropping whole buckets.
- Publish membership filters (Bloom or cuckoo) per zone and resolution, composable up the hierarchy, to answer "is anything in my layer here" without a scan.
- Treat LCS validity windows as leases renewed by a one-byte heartbeat so quiet frames cost nothing.

## G.8 Representations and the built environment (supports 7.6, 7.9, 17.1)

- **Resolve identifiers and candidates first.** Resolve every incoming record (parcel, asset register, IFC, CityGML, scan vendor, tileset feature, place id) against exact external identifiers, existing identities, and resolver candidate records before minting. Mint only after no acceptable match, subject to authorization. Duplicate identities are the most expensive mistake a twin makes, and they are made at ingestion.
- **Let BIM be the hierarchy where it exists.** IFC is already a transform tree: IfcBuildingStorey to floor, IfcSpace to unit and room, IfcWindow and IfcDoor to fixtures, IfcLocalPlacement to LCS transforms, GlobalId to `identified_as`. Resolve or declare BIM entities after the same check; submit externally computed scan-to-entity registration results to the resolver. Where no BIM exists, the scan-derived tree becomes the record and a later BIM submits its externally computed registration result.
- **Windows and doors are useful external correspondence anchors.** Use external grounding/matching/re-identification/SEGS and registration services for correspondence. Submit their candidate matches, evidence, confidence, and externally computed transforms to the resolver. The resolver records candidates; only an authorized decision may reuse or merge identities. 4D-ID stores the accepted result and provenance but does not perform matching or registration.
- **Floor index from height.** Facade window rows divided by declared slab height give physical floor index; the floor's display label is a separate field, because thirteen is skipped, ground is 0 in one city and 1 in another, and mezzanines exist.
- **Cut representations per room.** Splat clusters and meshes split per room carry their own `represents` relation and level of detail, so a client loads the room it is in.
- **Exterior to interior is a level-of-detail switch, not a portal.** Resolve the building, follow `represents`, choose by the visibility query's LOD hint, viewer capability, credential, and license. Because interior and exterior windows share identity, the swap does not jump. A license field on `represents` is what tells a client that a commercial tileset may be streamed but never cached into an almanac.
- **Scenarios are domains, not edits.** A proposed modification, whether drawn by a designer or generated by a model, is a scenario-mode domain derived from the real entity with a lease, the generating model in provenance, and proxies of structural and immovable elements carrying affordance truth. The proposal is an event entity with the real entity as subject, so "what was proposed for this facility in this interval" is an event query. If executed, the real entity receives a structural history event and the scenario is archived with a correspondence to it.

## G.9 Logical navigation between representations (supports Clause 18, 7.9)

Do not join the regional tileset, the site capture, and the interior scan into one continuous model. They differ in time, resolution, accuracy, vendor, and license, and joining them reconciles errors that resist reconciliation while costing the most at exactly the moment the user is moving. Resolve one identity down its hierarchy and hand off between representations instead.

- **One representation in view at a time.** Regional tiles at altitude, site capture at the perimeter, a single space's scan inside. Prefetch the next rung of the ladder (18.2) so the handoff has no load stall.
- **Obtain or compute registration externally before ingestion.** Store the externally computed interior-to-exterior transform, residual, and tier (7.8) as provenance. At runtime a client reads a cached transform; the candidate draft/client must not re-register live geometry.
- **Let the continuity anchor carry the cut.** Place the outgoing and incoming cameras relative to the anchor entity (18.3). Because the anchor is one identity with a pose in each representation, the fade lands on the same point. An opening is the ideal anchor between an exterior facade and an interior scan. This is what makes the leap feel like moving through the door rather than cutting to a slideshow.
- **Match the tier to the task.** Navigation and transitions run on logical or navigational registration; measurement and fit require metric (18.4). Ship the fluid experience before every unit is survey-registered, deferring the expensive solve until someone needs to measure.
- **Resolve to the freshest representation.** Follow `supersedes` and validity (7.9) so a stale interior is never shown as current unless history is requested.
- **The graph is instant; the geometry streams.** "What is inside this building and what represents it" is a kilobyte-scale relation query; the models it points to load on demand.

### Worked path: region to interior

1. Client shows the regional tileset; user selects a facility. Resolve the facility identity; read its LOD ladder.
2. Ladder rung 2 is the facility's approach viewpoint (18.1) framing the facade; camera flies there; exterior representation streams.
3. User selects a loading door. An external matching service grounds the facade and interior evidence to a candidate door; an authorized resolver accepts and records the result. The transition hint (18.3) names that identity as the continuity anchor.
4. Client positions the interior camera relative to the door's pose in the bay's scan, crossfades, and the door holds screen position. The bay scan is now in view; the exterior tileset is released.
5. Measurement in the bay switches to the metric-tier BIM or registered scan (18.4); browsing stays on the scan.

## G.10 Systems this family borrows from

| Source | Lesson taken |
|---|---|
| DNS; cellular home and visitor registers; locator/identifier separation | Delegated zones, home registers, caching with TTL, make-before-break handoff (14) |
| ROS tf2 | Time-indexed transform lookups, latched static transforms, bounded extrapolation, subtree subscription (7.6, 13.1) |
| ETSI Local Dynamic Map; GNSS almanac and ephemeris | Static versus dynamic substrate split (16.1) |
| ASTM Remote ID; UTM | Signed presence attestation as the compliance primitive (9.3) |
| VDA 5050 | AGV state as a 4D-State with motion extension; order and state separation (8) |
| Spanner TrueTime; hybrid logical clocks | Time as an interval; causally consistent ordering under skew (7.4) |
| Kafka; etcd; market-data feeds | Snapshot then stream; compacted last-value views; sequenced gap fill (16.5, 13.5) |
| Distributed simulation dead reckoning; game netcode | Threshold publishing, keyframes and deltas, priority budgets, interpolation buffers, time dilation (16.2, G.4, G.5) |
| Virtualized geometry and world partition in game engines | Aggregates as level of detail for state; GPU-driven culling (16.6, G.5) |
| Git; content-addressed storage | Immutable signed almanacs; digest reconciliation proportional to change (16.1, 16.4) |
| CRDT and single-writer practice | One authority per frame; availability under partition (14.3, 13.3) |

## G.11 Deferred items

Numbered for reference; none is required for conformance.

1. Learned-embedding profile alongside the canonical spatial feature vector, tagged per model and non-comparable across models.
18. Relation-type vocabulary beyond the six defined types, and whether an event ontology is warranted beyond events as entities; both are candidates for the taxonomy rather than the core.
19. Assured-profile mappings for specific classification and releasability regimes, maintained outside this family.
2. Foveated per-entity fidelity within one subscription, joining visibility hints to fan-out.
3. Multi-anchor graphs with well-formedness and disagreement resolution, once concrete drivers exist.
4. Reference pseudonymization scheme (k-anonymity cohorts, rotating pseudonyms, attribute-based credentials).
5. Disclosure and place-policy language, most likely an existing one (XACML, OPA Rego).
6. DGGS variant mandation or a translation layer, following standards-body engagement.
7. Standards-body track: OGC extension, joint OGC and Khronos item, independent, or permissively licensed. This decision shapes the others.
8. Semantic taxonomy and affordance vocabulary; discrete-state semantics; many-to-one and one-to-many views.
9. Normative definition of the `oct` grid and criteria for other synthetic grids.
10. External entity-resolution/re-identification interoperability and confidence semantics; no reference matcher in this family.
11. Authority election protocols for ad hoc co-located groups; nested local authority.
12. Relay topology and hot-zone splitting parameters; density forecasting inputs and their privacy implications.
13. Importance model for priority budgets.
14. Sensitive-place designation and contestation; proof-of-erasure as a verifiable protocol; traversal credential model; multi-sensor corroboration criteria; signature suites and delegation-chain encoding.
15. Human consent beyond proxying: a do-not-track layer or minimum disclosure resolution asserted by a person's own device.
16. Layer governance and registration; minting economics; cross-zone atomic structural updates.
17. Rigs for articulated proxies; portal rendering and audio; licensing references on views.

## G.12 Encoding Standard and reference implementation

Wire formats (JSON Schema, a binary form, and API surface) are deferred to a companion Encoding Standard produced with the reference implementation, which will fix serialization, ship executable versions of every Annex A test, provide reference conversions for GeoPose, Moving Features, VDA 5050, OpenXR, and glTF, and be published under Apache 2.0. Maintenance follows the outcome of G.11 item 7.

## G.13 Agent pattern and developer package

### Identify, understand, reason, act, observe, update

Actuation stays outside this family (17.3); a tool acts *on* a 4D-ID. The loop an agent runs:

1. **Identify.** Resolve exact external identifiers or submit externally generated candidate/grounding evidence to a resolver; a UI selection is not itself identity. `resolve` returns an accepted 4D-ID, candidate records, or a signed no-match result.
2. **Understand.** `context` returns a bounded envelope (10.6): class, labels, pose, affordances, relations, representations, provenance, constraints, all at a snapshot.
3. **Reason.** Follow `get_relations` and `query_events` as needed; never load geometry unless a representation is required for the purpose.
4. **Act.** Call a tool with the 4D-ID as the target (`inspect(door)`, `navigate_to(dock)`, `schedule(asset)`), scoped to the same snapshot and a policy scope.
5. **Observe.** The action's result returns as an observation or an event with agent-run provenance (7.8).
6. **Update.** Proposed changes enter as observations, candidate records, provisional identities only after no acceptable match, events, or scenario content and become authoritative only by authenticated promotion (7.9).

Delegation between agents carries the target 4D-ID, the snapshot, the policy scope, and evidence references (Part 1, B.4), so every agent in the chain refers to the same entity at the same version of the world.

### Developer package

Evaluation can begin in an afternoon. The companion package currently includes JSON Schema for records in Parts 1 to 5, an OpenAPI 3.1 description of the Clause 10 operations, a JavaScript SDK, a containerized candidate-recording/resolution service, conformance diagnostics, and sample data. Exactly 15 schema-level checks currently pass; broader functional conformance work continues. The IFC adapter is implemented; ROS 2 tf2, VDA 5050, glTF, 3D Tiles, OpenXR, major-engine adapters, MCP, and other SDKs remain planned unless their repositories say otherwise. These are external tools and clients consuming 4D-ID; the family does not provide a perception, matching, localization, registration, or rendering stack. The first experience should be four calls:

```
resolve(registry, id)      -> 4did:…
context(4did)              -> compact, agent-ready description
get_representations(4did)  -> scan / BIM / panorama / tiles, ranked for a purpose
watch(4did)                -> changes
```

*End of Part 6.*
