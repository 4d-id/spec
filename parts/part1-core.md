# 4D-ID™ 2.4, Part 1: Core

**Unified Spatiotemporal Identity for Shared Reality. Working draft offered for community review, Part 1 of 6.**

| | |
|---|---|
| Editors | D. Lorenzini and N. Lorenzini, Quantum Studio |
| Version | 2.4 (working draft) |
| Date | November 3, 2026 |
| Status | Working draft offered for community review. Not adopted by any standards body. |
| Track | Possible future OGC multi-part Implementation Standard; possible Khronos liaison item for OpenXR and glTF bindings; possible liaison targets include ROS 2, VDA 5050, ETSI ITS, and ASTM F38 communities |

## Abstract

4D-ID preserves a stable hierarchical identity for each resolved object, surface, agent, and environment, physical or virtual, with current state carrying an Earth-anchored global reference (OGC DGGS), a high-precision local frame, orientation (OGC GeoPose), and time (ISO 8601), independently of the identifier. It is an identity and continuity layer over existing coordinate systems; it is not a coordinate system, perception, grounding/matching, re-identification/SEGS, localization, registration, rendering, or ledger system.

This Part specifies the core: the identifier, the hierarchy, the state record, the time model, motion mode, local coordinate systems, transform conventions, uncertainty and provenance, lifecycle and relations, and the conformance framework for the whole family. Four concepts carry it: identity, hierarchy, pose, time. Parts 2 through 5 add optional requirements classes for extensions and access, privacy and security, planetary-scale operation, and domains and presentation. Part 6 is an informative implementation guide.

## Family map

| Part | Content | Requirements classes | Clauses |
|---|---|---|---|
| 1 Core | Identifier, hierarchy, state, time, LCS, conformance | `core` | 1 to 8 |
| 2 Extensions and access | Motion, history, presence, semantics; access operations, queries, context envelope, feature vector | `motion` `history` `presence` `semantics` `query` `features` | 9, 10 |
| 3 Privacy and security | Pseudonyms, disclosure, retention, consent, place policy; signed fabric, audit | `privacy` `security` | 11, 12 |
| 4 Planetary-scale architecture | Propagation and failure handling, resolution and authority, identity lifecycle, scale | `propagation` `fabric` `lifecycle` `scale` | 13 to 16 |
| 5 Domains, portals, proxies, presentation | Virtual, generated, and simulated spaces; cross-domain presence; cinematic navigation | `domain` `presentation` | 17, 18 |
| 6 Implementation guide | Informative techniques, agent patterns, systems borrowed from, deferred items, developer package | none | G.1 to G.13 |

Part 1 is usable as a standalone part/profile. Clause and requirement numbering is unique across the family (5.5).

---

## 1. Scope

This Part specifies an abstract data model for a persistent spatiotemporal identifier (the 4D-ID) and a transmitted state record (the 4D-State); a hierarchical anchoring model rooted in a Discrete Global Grid System and refined through local coordinate systems; a time model; motion modes; transform, unit, and axis conventions; uncertainty and provenance; identity lifecycle and derivation; alignment with OGC and Khronos standards; and the conformance framework for Parts 1 through 5.

It does not specify pose generation, perception, grounding/matching or re-identification (including SEGS), localization, registration, geometry production, discovery, rendering, or wire encoding. The family records and serves accepted externally produced outputs and evidence; the versioned [2.4 encoding working draft](../encoding/2.4.md) describes the partial JSON Schema and OpenAPI bindings and their limits (Part 6, G.12, G.13).

## 2. Conformance

A requirement is normative in this family only if two independent implementations would fail to interoperate without it. Techniques that improve performance or robustness inside one implementation are collected in Part 6 and carry no conformance weight.

### 2.1 Requirements classes

| Class | Part | Clause | Content |
|---|---|---|---|
| `core` | 1 | 7, 8 | Identifier, hierarchy, state record, time, motion mode, LCS, composition, uncertainty, lifecycle |
| `motion` | 2 | 9.1 | Velocity, acceleration, confidence decay |
| `history` | 2 | 9.2 | Bounded past and advisory future poses |
| `presence` | 2 | 9.3 | Signed attestation of pose at time |
| `semantics` | 2 | 9.4 | Class, affordance, hull, discrete state |
| `query` | 2 | 10 | Access operations (one semantic API, many bindings); hierarchical, temporal, relation, event, ray-cast, visibility queries; context envelope |
| `features` | 2 | 10.4 | Canonical spatial feature vector |
| `privacy` | 3 | 11 | Pseudonyms, scoped disclosure, retention, consent, place policy |
| `security` | 3 | 12 | Authenticated operations, signed fabric, disclosure inheritance, erasure, audit, assured labels and authenticated state |
| `propagation` | 4 | 13 | Region-keyed streaming, backpressure, priority, partition, fourteen failure classes |
| `fabric` | 4 | 14 | Zones, home registers, caching, handoff, single-writer authority |
| `lifecycle` | 4 | 15 | Resolution evidence/candidates, identity minting, authorized merge, split, leases, layers |
| `scale` | 4 | 16 | Almanac and ephemeris, threshold publishing, deltas, digests, snapshots, aggregates |
| `domain` | 5 | 17 | Domains, portals, proxies, views, domain time |
| `presentation` | 5 | 18 | Viewpoints, LOD ladder, transition hints, continuity anchors, registration tier |

### 2.2 Profiles

| Profile | Classes |
|---|---|
| P1 Static | `core` |
| P2 Dynamic | P1 + `motion` |
| P3 Temporal | P2 + `history` + `query` |
| P4 Verified | P3 + `presence` |
| P5 AI-Integrated | P3 or P4, + `semantics` + `features` + `query` |
| P6 Assured | P4 + `semantics` + `query` + `propagation` + `fabric` + `lifecycle` + `scale` + `security` in full (12.1 to 12.6) |

Profiles are layered. Any class may be claimed in addition to a profile; P5 and P6 combine (P6 + `features`), and `domain` is claimed with any profile that includes `lifecycle` (for example P6 + `domain`). `security` 12.1 is required by every profile; 12.2 to 12.5 bind to the classes they name; 12.6 is required only by P6. `privacy` is required wherever Clause 11 applies.

### 2.3 Conformance statement

A claim SHALL name the profile and additional classes; the DGGS variants supported; and, per class claimed, the parameters each clause marks *declared*. A claim without a profile is invalid.

## 3. Normative references

OGC 21-056r11 GeoPose 1.0 · OGC 20-040r3 DGGS Abstract Specification · OGC 21-038 OGC API: DGGS · OGC 18-075 Moving Features JSON · ISO 8601-1:2019 · ISO 19111:2019 · IETF RFC 2119, 8174, 3986, 5234, 9562 · W3C Verifiable Credentials Data Model 2.0 · Khronos OpenXR 1.1 · Khronos glTF 2.0

## 4. Terms

**4D-ID.** A persistent, opaque identifier for one entity (7.2).
**4D-State.** A record describing one entity at one moment (7.3).
**anchor.** The DGGS cell, at a declared resolution, containing an entity's position or a frame's extent.
**authority.** The producer designated for an accepted frame write scope (14.3); conferred and overlapping claims are attributed, bounded, and disputable (14.4), not self-authenticating.
**derivation.** A reference from a new 4D-ID to a prior 4D-ID when identity continuity breaks: fork, split, merge, replacement (7.9).
**domain.** A root frame with its own grid, clock, and authority; Earth is the domain whose grid is DGGS (17).
**entity.** Anything with a pose: object, surface, agent, sensor, reconstruction, virtual asset, environment.
**generation.** A monotonic counter on a node, incremented on any transform or parent change (16.4).
**genesis anchor.** The fixed DGGS minting/routing metadata in a legacy spatial identifier; never current location or grounding evidence.
**home token.** An opaque, non-spatial routing token in an `id`-variant identifier, independent of place, person, and time (7.2, 14.1).
**registration.** An externally supplied assertion relating an already identified entity to another frame, optionally with a transform; not a composition parent or identity decision (7.3, 7.8).
**layer.** A namespace identifier scoping entities and subscriptions (15.5).
**lease.** An expiry after which an unrenewed entity moves to terminal (15.5).
**Local Coordinate System (LCS).** A bounded, right-handed metric frame anchored to a parent (7.6).
**motion mode.** Static, physical, or teleportable (7.5).
**observation.** Externally produced evidence about a possible referent; never identity state, whether or not it has candidate associations (15.1).
**grounding.** Determining which real or virtual referent a record denotes.
**localization.** Estimating where a grounded referent is, in a stated frame.
**candidate match.** A non-authoritative, externally produced association between evidence and a possible 4D-ID, with evidence, provenance, and decision status.
**resolver.** A component that records and serves accepted IDs, candidate associations, and authorized lifecycle decisions; it does not perform perception, localization, matching, re-identification/SEGS, or registration.
**pose.** Position and orientation relative to the parent, expressed as GeoPose.
**relation.** A typed secondary reference between entities with validity, confidence, and provenance; never implies a transform (7.9).
**Spatial Entity Grounding Service (SEGS).** An adjacent implementation or service that may detect/segment, classify, track/re-identify, localize, and match observations to known entities before submitting evidence or candidate associations to 4D-ID. SEGS is not part of the core family.
**snapshot.** A vector of zone generations with a reference time and maximum skew, naming one coherent picture (16.5).
**viewpoint.** An entity with a pose that frames another entity, used to place a camera (18.1).
**continuity anchor.** The shared entity a client keeps fixed across a transition between representations (18.3).
**structural history.** A recorded change to an entity's structure or frame under which identity continues (7.9).
**producer, consumer.** A system that emits records; a system that receives them.
**proxy.** An entity whose pose is derived from a source entity in another frame (17.3).
**validity window.** The interval over which a pose or transform may be treated as current.
**zone.** A DGGS cell subtree with one authoritative resolver (14.1).

## 5. Conventions

**5.1** SHALL, SHOULD, and MAY are as in RFC 2119 and RFC 8174. Requirements are labeled `/req/<class>/<name>` and tested by `/conf/<class>/<name>` in Annex A of the Part that defines them.

**5.2 Units.** Meters, radians, SI seconds. Timestamps are ISO 8601 with UTC offset. Global positions are IEEE 754 binary64; binary32 is permitted within an LCS of extent at most 10 km. Quaternions are unit, (x, y, z, w), Hamilton convention. Matrices are 4×4, column-major, column-vector convention, as in glTF and OpenXR.

**5.3 Axes.** An LCS is right-handed, +Y up, +X right, −Z forward. GeoPose local tangent frames are East-North-Up. The mapping is fixed: LCS +X = East, +Y = Up, +Z = −North. No other mapping is conformant.

**5.4 Declared parameters.** Where a clause says a value is *declared*, the implementation states it in its conformance statement.

**5.5 Family numbering.** Clause, requirement, and test numbering is unique across Parts 1 to 5. A reference such as 14.2 denotes that clause in whichever Part carries it.

## 6. Overview (informative)

Spatial computing runs on frames that do not align: geographic (GIS, HD maps), device-local (headsets, robots), scene graphs (engines, simulators), odometry and map frames (robotics), and reconstruction frames (LiDAR, splats). These are adjacent producers and consumers. 4D-ID consumes their accepted externally produced grounding, localization, registration, and state results and provides a stable name for a resolved referent across movement, re-observation, system boundaries, and the boundary between real and virtual. The family does not perform perception, grounding/matching, re-identification/SEGS, localization, registration, or rendering.

```
  AI reasoning, planning, analytics       <- feature vector; relations; queries (Part 2)
  Fleet managers, twins, renderer clients, UTM <- 4D-State stream; almanac + ephemeris (Part 4)
  ------------------------------------------------------------------------------
  4D-ID: identity + hierarchy + pose + time (Part 1); domains (Part 5)
  ------------------------------------------------------------------------------
  OGC GeoPose · OGC DGGS · ISO 8601 · ROS tf2 · VDA 5050 · ETSI LDM · OpenXR · glTF
  ------------------------------------------------------------------------------
  SLAM, LiDAR, photogrammetry, sensor fusion, simulators, generative world models
```

4D-ID is not a coordinate system, not a replacement for GeoPose or DGGS, and not a perception, grounding/matching, re-identification/SEGS, localization, registration, rendering, blockchain, or discovery system. It uses GeoPose and DGGS, consumes accepted outputs from adjacent producers, records externally supplied results, allows signed attestation without a ledger, and pairs with registries and clients for discovery and rendering.

---

## 7. Core data model (requirements class: `core`)

### 7.1 Hierarchy

Composition is a nested transform tree, not a claim that every spatial relationship is a tree. Each non-root node has a 4D-ID, one composition parent, a local frame, a transform relative to that parent, a pose timestamp, and optional uncertainty, provenance, registrations, and extensions. The tree spans a domain root through region, facility, room, object, and sub-object. Many externally supplied registrations can relate a node to other frames without adding composition edges. Virtual entities can anchor in the same tree as physical ones.

> **/req/core/strict-tree**
> Each non-root entity SHALL have exactly one composition parent. An unembedded domain root (17.1) has none; an embedded domain root has exactly one. Writes introducing a second composition parent, self-parenting, or a composition cycle SHALL be rejected. Registrations and relations SHALL NOT add parents or participate in composition, tree traversal, depth, or tree cycle detection. Multi-parent composition is not defined in this family.

> **/req/core/depth**
> Implementations SHALL support at least 12 levels below the domain root, SHALL declare their maximum supported depth, and SHALL reject writes that would exceed it.

### 7.2 Identifier

A 4D-ID has a fixed home component and a local descriptor, with a genesis marker only where permitted below. Legacy spatial variants use a **genesis anchor** (DGGS variant, cell, optional vertical reference) as minting/routing metadata. The non-spatial variant `id` uses the same grammar with an opaque **home token** in the `cell` slot and no vertical reference or genesis marker. Neither form establishes the referent or its current location. All identifier components are fixed at minting; current anchors and valid, accepted registrations describe location independently of the name.

> **/req/core/identity-stable**
> A 4D-ID SHALL NOT change as the entity moves, ages, is re-measured, is restructured, changes frame, or is observed by different consumers, so long as continuity of the underlying entity remains authoritative. A vehicle keeps one 4D-ID across its service life; a building across renovation and extension; a robot across map reloads; an aircraft across hours out of contact.

> **/req/core/genesis-anchor**
> A legacy spatial genesis anchor records where the identity was minted and remains valid minting/routing metadata only. It SHALL NOT be treated as grounding evidence or as the entity's current location. The entity's current anchor SHALL be carried in the 4D-State and SHALL NOT be inferred from any identifier, including an `id` home token. Location SHALL be determined from current state and valid, accepted externally supplied registrations, subject to their frames, uncertainty, and validity.

> **/req/core/descriptor**
> A generated local descriptor SHALL be a UUID (RFC 9562) version 4 or 7, or SHALL carry at least 128 bits of entropy from a documented source. Consumers SHALL NOT infer the referent or current location from the descriptor; interpretation is limited to format validation and the legacy UUIDv7 genesis normalization below.

> **/req/core/genesis-implicit**
> For legacy spatial variants, when the descriptor is a UUIDv7 the genesis marker MAY be omitted; the genesis instant is then the UUIDv7 timestamp. Otherwise the marker SHALL be present. Implementations SHALL compare legacy spatial identifiers after normalizing to the explicit form. For variant `id`, the genesis marker SHALL be absent and normalization SHALL NOT synthesize one; comparison uses the unchanged canonical identifier bytes.

> **/req/core/genesis-privacy**
> Implementations SHALL accept the non-spatial variant `id` under the existing URI grammar. Its `cell` slot SHALL be an opaque home token generated independently with at least 128 bits of entropy from a documented cryptographically secure source; it SHALL encode no place, person, or time, including encoded or hashed derivatives of those values. Its local descriptor SHALL be a UUIDv4 or carry at least 128 bits of entropy from a documented cryptographically secure source, with no encoded place, person, or time. UUIDv7, a vertical reference, and a genesis timestamp SHALL NOT be used in this mode. Consumers SHALL NOT infer a domain, location, identity evidence, or mint time from an `id` identifier. Existing spatial identifiers SHALL remain resolvable without rewriting or reminting. Privacy-sensitive new identities SHOULD use `id`; access control and pseudonymization remain necessary because persistent names can still be correlated.

> **/req/core/uri-form**
> A 4D-ID SHALL be serializable to the following canonical form and compared byte-wise after the normalization defined above:
> ```
> fourd-id = "4did:" variant ":" cell [ ";v=" vref ] ":" local [ ":" genesis ]
> variant  = 1*8( ALPHA / DIGIT )            ; "id" for non-spatial home tokens; "h3", "s2", "isea3h", "oct"
> cell     = [ dom "." ] 1*64( ALPHA / DIGIT / "-" / "." )   ; legacy dom = domain-root descriptor; "id" uses an opaque home token
> vref     = datum / floorref
> datum    = 1*32( ALPHA / DIGIT / "-" )                     ; a vertical datum, e.g. "egm2008"
> floorref = "floor." 1*4( DIGIT / "-" ) [ "." 1*16( ALPHA / DIGIT / "-" ) ]   ; physical floor index, optional unit label
> local    = 22*86( ALPHA / DIGIT / "-" / "_" )              ; base64url, no padding
> genesis  = 8DIGIT "T" 6DIGIT [ "." 1*6DIGIT ] "Z"
> ```
> Examples: `4did:h3:8928308280fffff:AZmR3kB8dH2qT7vLxN1pWg` (UUIDv7, 48 characters); `4did:h3:8928308280fffff:Q3qP1zV9fT2xLmN8wK5aBg:20260503T141500Z`; `4did:h3:8928308280fffff;v=floor.12.b7:AZmR3kB8dH2qT7vLxN1pWg` (a space on the twelfth physical floor). Non-spatial example: `4did:id:6c986e8b29c144bb9c5701c8e9cf1564:Z6F5o8oBRvOS6zD4K1m2nQ` (random home token and UUIDv4 descriptor; neither identifies a place).

**Migration (informative).** Keep all existing IDs, references, and redirects unchanged. A resolver adds a declared home-token-to-home-register mapping (14.1), separate from its current-anchor indexes. Choose `id` for new privacy-sensitive minting only after the same existing-identity-first reconciliation as any other mint. Do not mint a second identity merely to change identifier mode or to conceal a legacy anchor. Legacy IDs may expose minting place/time; scoped disclosure and pseudonyms (Clause 11) mitigate exposure but cannot remove information already published. Domain membership comes from state/domain metadata, not an `id` token. The larger identifier/grid design and eventual default remain open for 2.5 (Part 6, G.11).

### 7.3 State record

> **/req/core/state-fields**
> A 4D-State SHALL carry: the 4D-ID; the parent 4D-ID or domain root; the current anchor (variant, cell, resolution); the pose relative to the parent as a GeoPose-compatible structure; source and publish time; a per-producer sequence number; a producer identifier; and a validity window. It MAY carry extensions (Part 2), uncertainty and provenance (7.8), lifecycle status and derivation (7.9), a discontinuity marker (7.5), a source-time bound (7.4), a disclosure policy reference (11.2), a layer and lease (15.5), a generation (16.4), a priority (13.2), and assured labels (12.6). It MAY carry `registrations`, a list of externally supplied registration records. Each record SHALL carry a target `frame` 4D-ID, tier (`logical`, `navigational`, or `metric`), confidence in [0, 1], a half-open validity interval (`valid_from` inclusive, `valid_to` exclusive, with end later than start), provenance (7.8), and status (`proposed`, `accepted`, `rejected`, `disputed`, `superseded`, or `expired`). An optional `transform` maps the entity local frame into the named registration frame under 5.2, 5.3, and 7.7; absence means no transform assertion, not an identity transform. Registration status SHALL be evaluated with validity; an expired or non-accepted registration SHALL NOT be consumed as current accepted placement. A registration SHALL NOT establish identity, alter `id`, replace `parent` or `pose`, or add a composition edge.

Two 4D-States sharing a 4D-ID describe one entity at two moments. The state `pose` remains relative to its sole composition parent regardless of registrations. A disputed or inconsistent registration is retained as attributed evidence, not silently blended into the parent pose. Unembedded domain roots are declared under 17.1, not represented by self-parented states.

### 7.4 Time

> **/req/core/timestamps**
> Every 4D-State SHALL carry source time (when the producer produced or accepted the pose assertion) and publish time (when it entered the propagation layer). Receivers SHALL stamp receive time on arrival and SHALL NOT forward it. Producers SHALL carry a source-time uncertainty bound in seconds, using a declared default where uncalibrated. Raw observations reference externally produced evidence; they are not authoritative identity state.

> **/req/core/sequence**
> Each producer SHALL stamp records with a sequence number strictly monotonic per 4D-ID. Gap and reorder detection SHALL use sequence numbers, not timestamps.

### 7.5 Motion mode

> **/req/core/motion-mode**
> Every entity SHALL declare one motion mode in its stable metadata: **static** (consumers SHALL NOT interpolate or extrapolate), **physical** (continuous motion; consumers MAY interpolate and extrapolate within the motion extension's confidence window), or **teleportable** (physical between discrete jumps; each jump SHALL be signaled). Producers SHALL NOT change a declared mode.

> **/req/core/discontinuity**
> A record following a discrete jump SHALL carry a discontinuity marker referencing the prior sequence number. Consumers SHALL invalidate predictions derived from the prior pose and SHALL NOT interpolate across the marker. A marker is intentional; a sequence gap is missing data.

### 7.6 Local Coordinate Systems

Fine geometry (point clouds, meshes, splats, skeletons) and control-rate computation live in an LCS: a bounded frame anchored to a parent 4D-ID.

> **/req/core/lcs**
> An LCS SHALL declare a bounded extent, a transform to its parent, a validity window, and a synchronization tolerance. It SHALL be anchored to the smallest DGGS cell fully containing its extent; when it grows beyond that cell it SHALL migrate to the next-coarser containing cell as a structural history event (7.9) with an unchanged identity.

> **/req/core/vertical-reference**
> A floor SHALL be an LCS whose parent is the building and which declares its physical index (counted from the lowest slab at 0), its display label (which MAY skip or rename floors), and its slab elevation relative to the building frame. A `floor.` vertical reference in an identifier SHALL name the physical index, never the label. A consumer holding only a horizontal position and a floor reference SHALL be able to derive a three-dimensional pose from the floor's declared elevation.

This is the contract a vertical geocoder relies on: address plus floor plus unit resolves through `identified_as` (7.9) to a unit 4D-ID, whose state gives a pose any two-dimensional client can lift into three.

> **/req/core/composition**
> The global pose of an entity SHALL equal the ordered product of parent transforms from the domain root, under 5.2 and 5.3, and SHALL agree with a reference chain walk within the entity's declared uncertainty. A cached composed transform SHALL be composed only through static-mode ancestors; below a moving ancestor, the global pose is obtained at read time by applying that ancestor's current pose.

### 7.7 Scale

> **/req/core/uniform-scale**
> A transform MAY carry a uniform scale s > 0. Non-uniform scale and shear SHALL NOT be used. Through a scaled transform, velocities and extents scale by s and covariances by s²; error budgets and halo distances declared in the child's units SHALL be converted at composition.

### 7.8 Uncertainty and provenance

> **/req/core/uncertainty**
> Uncertainty, where carried, SHALL be a 3×3 position covariance in the parent frame (six upper-triangular binary32 values, m²), an orientation standard deviation in radians or a 3×3 rotation-vector covariance, and a scalar confidence in [0, 1]. Absent uncertainty SHALL be treated as unknown, not zero.

> **/req/core/provenance**
> Provenance, where carried, SHALL identify the producing system and sensing or generation method. Registration provenance SHALL identify that external producer, method, evidence references, and assertion time (`registered`); the registration record carries its tier, confidence, validity, and status. Where a registration result against the composition parent is carried in state provenance, it SHALL include its tier and assertion time. An externally supplied RMS error in meters SHALL be carried when known; absent RMS means unknown, not zero. Tiers are **logical** (linked but not spatially registered), **navigational** (placed well enough to view and transition), and **metric** (survey-grade for measurement). A metric claim SHALL carry its externally supplied RMS error. If tier is repeated in registration provenance, the repeated value SHALL agree with the registration record. Neither tier nor confidence establishes identity or authority. The family records registration results; it does not compute registration. A state fused from several sources SHALL additionally carry the supporting observation references (15.1), the fusion authority, the fusion model and version, an identity confidence in [0, 1], and a state confidence in [0, 1]. State, relations, or events produced by an automated agent SHALL additionally carry the agent identifier, run identifier, task identifier, model and version, the input snapshot (16.5), evidence references, confidence, and approval status. Authority fields are attribution, not authentication or authorization proof (14.4).

One authoritative 4D-State, many contributing sensors, and a consumer can ask why the system believes what it believes.

### 7.9 Lifecycle and derivation

> **/req/core/lifecycle**
> Every 4D-ID SHALL be in one status: **provisional**, **active**, **offline_active**, **lost_contact**, **unanchored**, **merged**, or **terminal**. Loss of contact is a state of knowledge and SHALL NOT by itself cause termination; an entity returns from lost_contact through replay (13.5). Terminal is entered only by destruction, retirement, lease expiry, or an authenticated termination record. Merged and terminal are irreversible; records under a merged or terminal 4D-ID SHALL be rejected.

> **/req/core/structural-history**
> A change to an entity's structure, extent, or frame under which continuity is authoritative (a building gains a wing, a vehicle is refitted, an LCS migrates cells, authority transfers) SHALL be recorded as a structural history event carrying a generation increment (16.4), the change class, and provenance. It SHALL NOT mint a new identity.

> **/req/core/derivation**
> After initial identity creation under 7.10, a new identity replacing or branching from an existing one SHALL be minted only for a break in continuity (fork, split, or replacement by a distinct entity), with a derivation reference to the prior one, which SHALL remain resolvable within the declared retention window. Merge reuses its survivor under 15.2; it does not require another identity.

> **/req/core/labels**
> An entity MAY carry human-readable labels, each localized and each with source, validity, and provenance. Labels MAY change and SHALL NOT determine identity; `identified_as` (below) remains the mechanism for authoritative external identifiers.

> **/req/core/promotion**
> Content produced by inference or automation (a detected object, an inferred relation, a proposed change) SHALL enter as an observation/evidence record, candidate evidence, event (9.4), or scenario-domain content (17.1). After the resolve-first check, a resolver MAY mint a provisional identity only after a valid `no_acceptable_match` decision under 7.10; any such identity SHALL become authoritative state in the Earth domain only through authenticated promotion by the responsible authority (12.1). Automation proposes; authority promotes.

> **/req/core/relation**
> An entity MAY carry typed relations to other 4D-IDs. Each relation SHALL carry a type, a validity interval, a confidence in [0, 1], and provenance. This family defines six types: `proxy_of` (17.3), `portal` (17.2), `corresponds_to` (17.6), `observed_by` (15.1), `represents`, and `identified_as`; further types come from the namespaced taxonomy of 9.4. A relation SHALL NOT imply a transform and SHALL NOT participate in composition, traversal, depth, or cycle detection.

> **/req/core/represents**
> A `represents` relation links a representation entity (a point cloud, splat, mesh, panorama set, BIM model, or tileset, each with its own LCS and externally supplied registration result) to the entity it depicts. It SHALL carry the representation kind, capture time, level of detail, registration quality and tier (7.8), and a license reference, and MAY carry a validity window and a `supersedes` reference to an older representation it replaces. The registration tier (7.8) is recorded provenance; a consumer MAY prefer the highest-tier representation available as input to an external localization service and SHALL surface the tier when a lower one is used. A representation SHALL NOT be a proxy: it attaches geometry; it does not derive pose. A consumer resolving an entity's representations SHALL, absent a request for history, select the current one by validity and capture time.

> **/req/core/identified-as**
> An `identified_as` relation records an identifier for the entity in an external registry (a parcel number, an asset tag, an IFC GlobalId, a CityGML id, a scan vendor's model id, a tileset feature id, a place id). It SHALL carry the registry name and the identifier. Ingestion SHALL first attempt resolution using an exact/authorized external identifier and any resolver candidate records. If an acceptable existing identity is found, it SHALL be reused; only after a valid `no_acceptable_match` decision under 7.10 may authorized minting proceed. Vendor labels alone SHALL NOT establish identity.

Containment and attachment are expressed by the tree, not by relations. The relation graph is what planners and AI reason over; the tree is what renderer/controller clients consume for composition. Candidate associations, if exposed separately by a resolver, are non-authoritative evidence and SHALL NOT change identity or state. A facility with a parcel record, an IFC model, three LiDAR scans, a panorama capture, and an exterior tileset is one identity with several `identified_as` and several `represents` relations.

### 7.10 Bounded reconciliation

Reconciliation records a decision about externally grounded evidence and existing identities; it does not perform grounding or matching. The boundary is **OBSERVE -> GROUND -> IDENTIFY -> RESOLVE -> INTEROPERATE**: observations are evidence, grounding determines the referent, localization determines where, and 4D-ID preserves which resolved referent continues. SEGS and other grounding/localization services remain adjacent.

> **/req/core/reconciliation**
> Before minting or accepting an identity association, a resolver SHALL record a bounded reconciliation decision with a decision identifier, externally supplied evidence references and provenance, considered candidate references, the responsible authority's attribution, a policy reference, the lookup scope (registries, authorities, and indexes consulted), finite limits (maximum lookups, candidates, and elapsed time), completion and exhaustion indicators, decision time, and expiry later than that time. It SHALL first check exact/authorized identifiers and acceptable existing identities. It SHALL return one of five explicit outcomes: `reuse` (an acceptable existing identity, with its selected 4D-ID), `no_acceptable_match` (completed lookup within the declared scope, without an acceptable match), `ambiguous` (insufficient or non-unique evidence), `conflict` (incompatible identity or authority assertions), or `rejected` (invalid, unauthorized, or policy-disallowed input), with a reason. A known acceptable existing identity SHALL be reused, not duplicated. Incomplete, unavailable, truncated, or budget-exhausted lookup SHALL NOT be reported as `no_acceptable_match`; it SHALL return `ambiguous`, `conflict`, or `rejected` with the limitation recorded. A negative is scoped and time-bounded, not a claim of global absence. Only an unexpired `no_acceptable_match` decision whose scope and policy cover the proposed mint MAY permit minting, subject to authentication, authorization, and lifecycle rules. Other outcomes SHALL NOT mint automatically. Expired decisions SHALL be re-evaluated before action. Candidate records and the decision record alone SHALL NOT mutate identity, merge, split, re-parent, promote, or overwrite state; any such change requires a separately authorized lifecycle operation with evidence and provenance.

## 8. Alignment

> **/req/core/dggs-variant**
> Implementations SHALL declare each DGGS variant they support; spatial anchor records SHALL identify their variant. The identifier variant `id` is not a grid and SHALL NOT be used as a current-anchor or domain-grid variant. Where two variants or two resolutions meet, the receiver SHALL coerce to the coarser resolution (13.6) and emit a loss-of-precision indicator.

> **/req/core/geopose**
> Each 4D-State pose SHALL be expressible as GeoPose 1.0: Basic-Quaternion relative to a local tangent plane, Advanced relative to an arbitrary parent.

Informative. The motion and history extensions convert losslessly to OGC Moving Features. 3D Tiles tilesets and content are entities whose tile-local geometry lives in an LCS. The LCS hierarchy carries the semantics of ROS tf2 (latched statics, time-indexed lookups, bounded extrapolation) across the wide area; VDA 5050 AGV state maps onto a 4D-State with the `motion` extension; the ETSI Local Dynamic Map's permanent, transient, and dynamic layers map onto almanac and ephemeris (16.1). OpenXR and glTF bindings are proposed in Annex B.

---

## Annex A (normative). Tests for `core`

| Test | Method | Purpose |
|---|---|---|
| `/conf/core/strict-tree` | F | Reject two parents, self-parenting, and a composition cycle; accept one parent with several registrations, including reciprocal frame references; verify registrations do not change composition, depth, traversal, or identity. Verify unembedded and embedded domain-root handling. |
| `/conf/core/depth` | I, F | Verify declared maximum of at least 12; build to the maximum; attempt one more; expect rejection. |
| `/conf/core/identity-stable` | F | Move, re-measure, restructure, and re-observe an entity across 1,000 records and a loss of contact; verify unchanged 4D-ID. |
| `/conf/core/genesis-anchor` | D | Move an entity across cells; verify identifier unchanged and state anchor updated. |
| `/conf/core/descriptor` | I, D | Verify descriptor form and entropy source. |
| `/conf/core/genesis-implicit` | D | Verify legacy spatial UUIDv7 implicit/explicit normalization and required genesis otherwise; verify `id` comparison never synthesizes a timestamp. |
| `/conf/core/genesis-privacy` | I, D, F | Accept `id` in the existing grammar; inspect independent entropy sources and absence of encoded/hashed place, person, or time; reject UUIDv7, vertical reference, and genesis timestamp in this mode. Verify unchanged legacy resolution, non-spatial home routing, and location from state/registrations, never ID bytes. |
| `/conf/core/uri-form` | D | Round-trip through the grammar; verify byte-wise equality. |
| `/conf/core/state-fields` | D, F | Validate mandatory fields and scalar composition parent; accept zero or many registrations; validate frame, optional transform direction/shape, tier, confidence, ordered validity, provenance and status. Reject extra parent fields; verify absent transforms are unknown and expired/non-accepted placements are not current. |
| `/conf/core/timestamps` | D | Verify source and publish times and bound on emission; verify receive time not forwarded. |
| `/conf/core/sequence` | F | Inject reordered and missing records; verify detection. |
| `/conf/core/motion-mode` | F | Verify one declared mode; attempt a mode change; expect rejection. |
| `/conf/core/discontinuity` | F | Teleport an entity; verify marker and discarded predictions. |
| `/conf/core/vertical-reference` | D, F | Verify floor index, label, and elevation declared; resolve a floor reference with a horizontal position to a 3D pose. |
| `/conf/core/lcs` | F | Create an LCS straddling cells; verify coarser containing cell; grow it; verify migration as structural history with unchanged identity. |
| `/conf/core/composition` | F | Compare cached global poses to a chain walk over 10,000 entities; move a parent with 10,000 children; verify correct poses and no cache through the moving parent. |
| `/conf/core/uniform-scale` | F | Compose through a 1:1000 embedding; verify scaling of velocity and covariance; verify shear rejected. |
| `/conf/core/uncertainty` | D | Validate covariance layout and confidence range. |
| `/conf/core/provenance` | D, F | Validate producer/method and each registration's evidence, assertion time, consistent repeated tier, status and metric RMS; retain disagreements as attributed evidence, not blended state. Verify absent RMS is unknown; for fused and agent-produced state validate supporting observations, authority/model, confidences and agent-run provenance. |
| `/conf/core/lifecycle` | F | Take an entity through lost_contact and back; verify records accepted on return; drive it to terminal by authenticated termination; verify subsequent records rejected. |
| `/conf/core/structural-history` | F | Add a wing to a building; verify same 4D-ID, generation increment, history event. |
| `/conf/core/derivation` | F | Fork an entity; verify new 4D-ID with derivation; verify prior resolvable. |
| `/conf/core/labels` | D, F | Add and change labels; verify identity and `identified_as` unaffected. |
| `/conf/core/promotion` | F | Submit agent-generated content directly as Earth-domain state; verify refusal; promote with authority; verify acceptance and provenance. |
| `/conf/core/relation` | D, F | Validate type, validity, confidence, provenance; add relations forming a cycle; verify composition and cycle detection unaffected. |
| `/conf/core/represents` | D, F | Attach a splat and a BIM model to one unit; validate kind, capture time, LOD, registration, tier, license; supersede one; verify the current one is selected absent a history request; verify neither alters the unit's pose. |
| `/conf/core/identified-as` | F | Ingest the same facility from two registries; verify existing-identity reuse and two `identified_as` relations; verify ambiguous candidates do not mint and a no-acceptable-match result permits authorized minting. |
| `/conf/core/dggs-variant` | F | Exchange records at two resolutions; verify coercion and indicator. |
| `/conf/core/geopose` | D | Convert an LCS pose to GeoPose Basic and back; verify identity to 1e-9 relative. |
| `/conf/core/reconciliation` | I, D, F | Exercise reuse, no acceptable match, ambiguous, conflict, and rejected with scoped evidence, provenance, authority, finite limits and expiry. Verify only completed, unexhausted, unexpired negatives allow authorized minting; unavailable, truncated, exhausted, expired or ambiguous lookups do not. Submit candidates and decisions alone; verify no state, identity, parent, merge or promotion mutation. |

## Annex B (informative). Bindings

The access operations of Clause 10 are one semantic API with many bindings. None of the bindings below is normative.

### B.1 Khronos OpenXR
**Possible `XR_EXT_spatial_entity_4did`.** `xrGet4DIDForSpatialEntityEXT` submits an external grounding result or explicit authorized mint request and returns the resolved 4D-ID of a runtime spatial entity or anchor; resolution first checks existing identities. `xrCreateSpaceFrom4DIDEXT` resolves a 4D-ID to an `XrSpace`. `xrGet4DStateEXT` returns the 4D-State for a space at a predicted display time. The runtime's reference space is an LCS whose parent is the nearest anchored 4D-ID; because of 5.3 the axis mapping is identity.

### B.2 Khronos glTF
**Possible `EXT_4did_anchor`.** A node-level extension carrying `id`, `parent`, `anchorTransform` (16 floats, column-major, node to parent LCS), `motionMode`, and externally supplied `registration` metadata. A scene-level anchor with unanchored children implies LCS-local children. 3D Tiles tilesets carry the same object at tileset and content level; the binding carries registration results and does not calculate them.

### B.3 Model Context Protocol
The stateless MCP core routes each request on its own headers, returns cache hints on list and resource reads, and recommends explicit handles returned by tools and passed back as arguments over transport-hidden state. A 4D-ID and a snapshot id are such handles. Mapping: `4did:` identifiers are MCP resources; the Clause 10 operations are tools with JSON Schema inputs and outputs; long-running work (ingesting an externally grounded scan/result, recording an externally registered reconstruction, generating a scenario domain) uses MCP Tasks; the context envelope (10.6) is the default tool result for an entity. MCP carries context, discovery, queries, and actions. It does not carry the 4D-State stream (13); robots, headsets, vehicles, and renderer clients stay on that path. MCP operations expose resolver/query and candidate-recording functions only; they do not perform perception, matching, localization, registration, or rendering.

### B.4 Agent-to-agent delegation
Where one agent hands work to another, the delegated task carries a target 4D-ID, a snapshot id (16.5), a policy scope, and evidence references, so both agents refer to exactly the same entity at the same version of the world. The pattern is protocol-independent.

## Annex C (informative). Illustrative 4D-State

```json
{ "id": "4did:h3:8928308280fffff:AZmR3kB8dH2qT7vLxN1pWg",
  "parent": "4did:h3:8828308281fffff:R7kLm2Nq4sTvWx9yZa1bCd",
  "anchor": { "variant": "h3", "cell": "8928308280fffff", "resolution": 9 },
  "status": "active", "motion_mode": "physical", "layer": "public", "generation": 17,
  "pose": { "position": [12.417, 1.102, -3.884], "orientation": [0, 0.7071068, 0, 0.7071068] },
  "time": { "source": "2026-09-04T17:22:41.183Z", "bound_s": 0.004, "publish": "2026-09-04T17:22:41.201Z" },
  "producer": "agv:fleet-b:07", "sequence": 48211, "validity_s": 0.5,
  "uncertainty": { "position_cov_upper": [4e-4, 0, 0, 4e-4, 0, 9e-4], "orientation_sigma_rad": 0.004, "confidence": 0.93 },
  "provenance": { "producer": "agv:fleet-b:07", "method": "lidar-slam", "tier": "navigational", "rms_m": 0.011, "registered": "2026-09-04T17:20:00Z" },
  "ext": { "motion": { "velocity": [0.8, 0, -0.2], "confidence": 0.91 } } }
```

## Annex D (informative). Design rationale

Thirteen decisions a reviewer is likely to contest, with alternatives and reasons.

1. **Identity layer, not coordinate system.** Alternative: a unified frame. Every domain keeps its native frame; a new one is a sixth silo. What none of them has is a stable name.
2. **DGGS routes, partitions, and filters; it is not the name.** Alternative: make the spatial index determine identity. DGGS cells support spatial routing, partitions, queries, and level of detail while a persistent 4D-ID names the resolved referent. Changing grid, resolution, or location does not change identity.
3. **One composition parent, many registrations.** Alternative: turn every externally supplied alignment into a parent. A strict tree bounds traversal and makes composition unique, while independent registration records retain frame, transform, quality, validity, and provenance without changing identity or adding edges. Solving registration disagreements remains external.
4. **Separate identity from spatial indexing without breaking old names.** Legacy spatial genesis anchors remain valid mint/routing metadata, never grounding or current location. The grammar-compatible `id` mode supplies a non-spatial home token and random descriptor without place/person/time leakage; current anchors and registrations carry location. A larger identifier/grid redesign remains open for 2.5 rather than silently reminting existing identities.
5. **Identity follows continuity, not structure.** Alternative: mint on structural change. A building that gains a wing is the same building; a bridge is the same bridge across a decade of retrofits; an aircraft out of contact for hours is the same aircraft. Structure is history; a fork, split, or replacement can create a new identity, while an authorized merge reuses an existing survivor (15.2).
6. **Three timestamps with a bound.** Alternative: one timestamp or mandated synchronization. Planetary clock skew is unbounded in practice; carrying the bound turns drift into a number.
7. **Motion mode as stable metadata.** Interpolation rules must be known before the first record arrives.
8. **One fixed axis mapping.** Alternative: declared per implementation. Graphics is +Y up, geospatial is ENU, and ambiguity between them is the most common shared-reality defect.
9. **Cache through static ancestors only.** Alternative: cache everything with push invalidation. A moving ship with ten thousand containers would invalidate ten thousand caches per update.
10. **Availability over consistency on partition** (13.4). A vehicle in a tunnel and a robot in a basement keep operating; staleness is marked, never hidden.
11. **Signed attestations, not a ledger** (9.3). Proof of presence needs a signature, not consensus.
12. **Representations share identity; they are not joined into one model.** Alternative: reproject every capture into one continuous space. Captures differ in time, resolution, accuracy, vendor, and license, and forcing them together reconciles errors that do not want to reconcile. Sharing identity and transitioning between representations (Clause 18) is honest, cheap, and fluid; a joined model is none of the three.
13. **Privacy and security as requirements** (Part 3). A pose stream with history and prediction is a surveillance system unless the draft requires otherwise, and the substrate is the only layer positioned to enforce the rule across applications.

## Annex E (informative). Change history

| Version | Change |
|---|---|
| 2.4 (November 3, 2026) | Working draft offered for community review; 112 normative tests. Added privacy-preserving `id` home tokens, bounded reconciliation, and conferred/overlapping/disputed authority; one composition parent plus many external registrations; versioned partial encoding binding. Boundary clarification: grounding determines the referent, localization determines where, and 4D-ID preserves resolved identity continuity; observations are evidence; resolution is existing-identity-first and minting follows only when no acceptable match exists; externally supplied candidate associations and authorized lifecycle decisions may be recorded by resolvers; perception, matching/re-identification/SEGS, localization, registration, and rendering remain external. |
| 2.3 | Clause 10 rewritten as access operations (one semantic API, many bindings) with relation and event queries, purpose-based representation negotiation, snapshot access, watch, and a bounded context envelope. P5 requires `semantics`. Labels (non-identity) and the promotion rule (automation proposes, authority promotes) in 7.9; agent-run provenance in 7.8. MCP and agent-delegation bindings in Annex B. Feature-vector depth field bounded. Family map, scope pointers, and depth wording corrected. Part 6 gains agent pattern and developer package. |
| 2.2 | `localization` affordance and quality (9.4); registration tier on exterior representations (7.9); overlay-confidence rule (18.5). |
| 2.1 | `presentation` class: viewpoints, LOD ladder, transition hints, continuity anchors (Clause 18). Registration tier added to provenance (7.8). `represents` gains validity and `supersedes` (7.9). Implementation guide gains the logical-jump navigation pattern. Rationale entry on representations sharing identity rather than being joined. |
| 1.9 | `represents` and `identified_as` relations (7.9); vertical reference grammar and floor frames (7.2, 7.6); domain mode (17.1); built-environment affordances and namespace (9.4). N. Lorenzini added as co-editor. |
| 1.8 | External review incorporated: identity continuity principle and structural history (7.2, 7.9); `lost_contact` status, terminal reserved for authoritative termination (7.9, 13.4); depth as declared minimum (7.1); observations as ephemeral evidence with a record shape (15.1); fused-state provenance (7.8); typed relations with validity, confidence, provenance (7.9); events as entities (9.4); coherent snapshots (16.5); authority-assigned priority (13.2); assured security subclause (12.6); `embedding` renamed `features`; P6 Assured added, -S qualifier retired. |
| 1.7 | Applied the interoperability rule (2): normative requirements reduced from about 140 to about 75; classes from 20 to 14 (`lcs` into `core`; `query-*` into `query`; `resolution` and `authority` into `fabric`; `failure` into `propagation`; `identity-lifecycle` renamed `lifecycle`). Implementation techniques, systems borrowed from, and deferred items moved to Part 6. Rationale reduced to twelve entries. Examples balanced across robotics, automated driving, geospatial, XR, and AI. |
| 1.6 | Five-Part split; `realm` renamed `domain`, `projection` renamed `proxy`; genesis implicit for UUIDv7. |
| 1.5 | Security promoted to a normative class. |
| 1.4 | Domains, portals, proxies, views, semantics, consent, place policy. |
| 1.3 | Planetary-scale architecture. |
| 1.2 | Standards-body form: requirements classes, RFC 2119, canonical identifier, axis conventions, embedding layout, tests, Khronos bindings. |
| 1.1 | Initial working draft (May 2026). |

*End of Part 1.*
