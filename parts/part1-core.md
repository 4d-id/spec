# 4D-ID 2.3, Part 1: Core

**Unified Spatiotemporal Identity for Shared Reality. Open Standard Working Draft, Part 1 of 6.**

| | |
|---|---|
| Editors | D. Lorenzini and N. Lorenzini, Quantum Studio |
| Version | 2.3 (working draft) |
| Date | September 2026 |
| Status | Working draft, offered for community review. Not yet adopted by any standards body. |
| Track | Proposed OGC multi-part Implementation Standard; Khronos liaison item for OpenXR and glTF bindings; liaison sought with ROS 2, VDA 5050, ETSI ITS, and ASTM F38 communities |

## Abstract

4D-ID assigns every object, surface, agent, and environment, physical or virtual, a stable hierarchical identity that binds an Earth-anchored global reference (OGC DGGS), a high-precision local frame, orientation (OGC GeoPose), and time (ISO 8601). It is an identity and addressing layer over existing coordinate systems; it is not a coordinate system, a perception system, a rendering format, or a ledger.

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

Part 1 is adoptable on its own. Clause and requirement numbering is unique across the family (5.5).

---

## 1. Scope

This Part specifies an abstract data model for a persistent spatiotemporal identifier (the 4D-ID) and a transmitted state record (the 4D-State); a hierarchical anchoring model rooted in a Discrete Global Grid System and refined through local coordinate systems; a time model; motion modes; transform, unit, and axis conventions; uncertainty and provenance; identity lifecycle and derivation; alignment with OGC and Khronos standards; and the conformance framework for Parts 1 through 5.

It does not specify pose generation, geometry representation, discovery, or wire encoding. Encoding is the subject of a companion Encoding Standard and developer package (Part 6, G.12, G.13).

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
| `lifecycle` | 4 | 15 | Observations as evidence, identity minting, merge, split, leases, layers |
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
**authority.** The single producer whose records for a frame are accepted (14.3).
**derivation.** A reference from a new 4D-ID to a prior 4D-ID when identity continuity breaks: fork, split, merge, replacement (7.9).
**domain.** A root frame with its own grid, clock, and authority; Earth is the domain whose grid is DGGS (17).
**entity.** Anything with a pose: object, surface, agent, sensor, reconstruction, virtual asset, environment.
**generation.** A monotonic counter on a node, incremented on any transform or parent change (16.4).
**genesis anchor.** The DGGS cell in which a 4D-ID was minted; part of the identifier.
**layer.** A namespace identifier scoping entities and subscriptions (15.5).
**lease.** An expiry after which an unrenewed entity moves to terminal (15.5).
**Local Coordinate System (LCS).** A bounded, right-handed metric frame anchored to a parent (7.6).
**motion mode.** Static, physical, or teleportable (7.5).
**observation.** A detection not yet matched to an identity; exchangeable as ephemeral evidence, never as identity state (15.1).
**pose.** Position and orientation relative to the parent, expressed as GeoPose.
**relation.** A typed secondary reference between entities with validity, confidence, and provenance; never implies a transform (7.9).
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

Spatial computing runs on frames that do not align: geographic (GIS, HD maps), device-local (headsets, robots), scene graphs (engines, simulators), odometry and map frames (robotics), and reconstruction frames (LiDAR, splats). The standards for each are mature. What is missing is a stable name for a thing that survives movement, re-observation, system boundaries, and the boundary between real and virtual, with the latency and legibility that fleets, vehicles, headsets, and AI systems require at runtime. 4D-ID is that name and the minimum machinery around it.

```
  AI reasoning, planning, analytics       <- feature vector; relations; queries (Part 2)
  Fleet managers, twins, renderers, UTM   <- 4D-State stream; almanac + ephemeris (Part 4)
  ------------------------------------------------------------------------------
  4D-ID: identity + hierarchy + pose + time (Part 1); domains (Part 5)
  ------------------------------------------------------------------------------
  OGC GeoPose · OGC DGGS · ISO 8601 · ROS tf2 · VDA 5050 · ETSI LDM · OpenXR · glTF
  ------------------------------------------------------------------------------
  SLAM, LiDAR, photogrammetry, sensor fusion, simulators, generative world models
```

4D-ID is not a coordinate system, not a replacement for GeoPose or DGGS, not a perception system, not a rendering format, not a blockchain, and not a discovery mechanism. It uses the first two, consumes the output of the third, anchors the fourth, allows signed attestation without the fifth, and pairs with a registry for the sixth.

---

## 7. Core data model (requirements class: `core`)

### 7.1 Hierarchy

Spatial reality is a nested transform tree. Each node has a 4D-ID, a parent, a local frame, a transform relative to the parent, a pose timestamp, and optional uncertainty, provenance, and extensions. The tree spans a domain root (Earth, rooted in DGGS) through region, facility, room, object, and sub-object. Virtual entities anchor in the same tree as physical ones.

> **/req/core/strict-tree**
> Each entity SHALL have exactly one parent. Multi-parent composition is not defined in this family.

> **/req/core/depth**
> Implementations SHALL support at least 12 levels below the domain root, SHALL declare their maximum supported depth, and SHALL reject writes that would exceed it.

### 7.2 Identifier

A 4D-ID has three parts: a **genesis anchor** (DGGS variant, cell, optional vertical reference) recording where the identity was minted; a **local descriptor** unique within that anchor; and a **genesis marker** recording when it was minted. All three are fixed at minting.

> **/req/core/identity-stable**
> A 4D-ID SHALL NOT change as the entity moves, ages, is re-measured, is restructured, changes frame, or is observed by different consumers, so long as continuity of the underlying entity remains authoritative. A vehicle keeps one 4D-ID across its service life; a building across renovation and extension; a robot across map reloads; an aircraft across hours out of contact.

> **/req/core/genesis-anchor**
> The anchor in the identifier records where the identity was minted. The entity's current anchor SHALL be carried in the 4D-State and SHALL NOT be inferred from the identifier.

> **/req/core/descriptor**
> A generated local descriptor SHALL be a UUID (RFC 9562) version 4 or 7, or SHALL carry at least 128 bits of entropy from a documented source. Consumers SHALL NOT interpret the descriptor.

> **/req/core/genesis-implicit**
> When the descriptor is a UUIDv7 the genesis marker MAY be omitted; the genesis instant is then the UUIDv7 timestamp. Otherwise the marker SHALL be present. Implementations SHALL compare identifiers after normalizing to the explicit form.

> **/req/core/uri-form**
> A 4D-ID SHALL be serializable to the following canonical form and compared byte-wise:
> ```
> fourd-id = "4did:" variant ":" cell [ ";v=" vref ] ":" local [ ":" genesis ]
> variant  = 1*8( ALPHA / DIGIT )            ; "h3", "s2", "isea3h"; "oct" for virtual domains
> cell     = [ dom "." ] 1*64( ALPHA / DIGIT / "-" / "." )   ; dom = domain-root descriptor, absent on Earth
> vref     = datum / floorref
> datum    = 1*32( ALPHA / DIGIT / "-" )                     ; a vertical datum, e.g. "egm2008"
> floorref = "floor." 1*4( DIGIT / "-" ) [ "." 1*16( ALPHA / DIGIT / "-" ) ]   ; physical floor index, optional unit label
> local    = 22*86( ALPHA / DIGIT / "-" / "_" )              ; base64url, no padding
> genesis  = 8DIGIT "T" 6DIGIT [ "." 1*6DIGIT ] "Z"
> ```
> Examples: `4did:h3:8928308280fffff:AZmR3kB8dH2qT7vLxN1pWg` (UUIDv7, 48 characters); `4did:h3:8928308280fffff:Q3qP1zV9fT2xLmN8wK5aBg:20260503T141500Z`; `4did:h3:8928308280fffff;v=floor.12.b7:AZmR3kB8dH2qT7vLxN1pWg` (a space on the twelfth physical floor).

### 7.3 State record

> **/req/core/state-fields**
> A 4D-State SHALL carry: the 4D-ID; the parent 4D-ID or domain root; the current anchor (variant, cell, resolution); the pose relative to the parent as a GeoPose-compatible structure; source and publish time; a per-producer sequence number; a producer identifier; and a validity window. It MAY carry extensions (Part 2), uncertainty and provenance (7.8), lifecycle status and derivation (7.9), a discontinuity marker (7.5), a source-time bound (7.4), a disclosure policy reference (11.2), a layer and lease (15.5), a generation (16.4), a priority (13.2), and assured labels (12.6).

Two 4D-States sharing a 4D-ID describe one entity at two moments.

### 7.4 Time

> **/req/core/timestamps**
> Every 4D-State SHALL carry source time (when the producer observed the pose) and publish time (when it entered the propagation layer). Receivers SHALL stamp receive time on arrival and SHALL NOT forward it. Producers SHALL carry a source-time uncertainty bound in seconds, using a declared default where uncalibrated.

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
> Provenance, where carried, SHALL identify the producing system, the sensing or generation method, the registration RMS error in meters, the registration tier (**logical**: linked but not spatially registered; **navigational**: placed well enough to view and transition; **metric**: survey-grade for measurement), and the time of last registration against the parent. A state fused from several sources SHALL additionally carry the supporting observation references (15.1), the fusion authority, the fusion model and version, an identity confidence in [0, 1], and a state confidence in [0, 1]. State, relations, or events produced by an automated agent SHALL additionally carry the agent identifier, run identifier, task identifier, model and version, the input snapshot (16.5), evidence references, confidence, and approval status.

One authoritative 4D-State, many contributing sensors, and a consumer can ask why the system believes what it believes.

### 7.9 Lifecycle and derivation

> **/req/core/lifecycle**
> Every 4D-ID SHALL be in one status: **provisional**, **active**, **offline_active**, **lost_contact**, **unanchored**, **merged**, or **terminal**. Loss of contact is a state of knowledge and SHALL NOT by itself cause termination; an entity returns from lost_contact through replay (13.5). Terminal is entered only by destruction, retirement, lease expiry, or an authenticated termination record. Merged and terminal are irreversible; records under a merged or terminal 4D-ID SHALL be rejected.

> **/req/core/structural-history**
> A change to an entity's structure, extent, or frame under which continuity is authoritative (a building gains a wing, a vehicle is refitted, an LCS migrates cells, authority transfers) SHALL be recorded as a structural history event carrying a generation increment (16.4), the change class, and provenance. It SHALL NOT mint a new identity.

> **/req/core/derivation**
> Only a break in identity continuity (fork, split, merge, replacement by a distinct entity) SHALL mint a new 4D-ID, with a derivation reference to the prior one, which SHALL remain resolvable within the declared retention window.

> **/req/core/labels**
> An entity MAY carry human-readable labels, each localized and each with source, validity, and provenance. Labels MAY change and SHALL NOT determine identity; `identified_as` (below) remains the mechanism for authoritative external identifiers.

> **/req/core/promotion**
> Content produced by inference or automation (a detected object, an inferred relation, a proposed change) SHALL enter as an observation (15.1), a provisional identity, an event (9.4), or scenario-domain content (17.1), and SHALL become authoritative state in the Earth domain only through an authenticated promotion by the responsible authority (12.1). Automation proposes; authority promotes.

> **/req/core/relation**
> An entity MAY carry typed relations to other 4D-IDs. Each relation SHALL carry a type, a validity interval, a confidence in [0, 1], and provenance. This family defines six types: `proxy_of` (17.3), `portal` (17.2), `corresponds_to` (17.6), `observed_by` (15.1), `represents`, and `identified_as`; further types come from the namespaced taxonomy of 9.4. A relation SHALL NOT imply a transform and SHALL NOT participate in composition, traversal, depth, or cycle detection.

> **/req/core/represents**
> A `represents` relation links a representation entity (a point cloud, splat, mesh, panorama set, BIM model, or tileset, each with its own LCS and registration) to the entity it depicts. It SHALL carry the representation kind, capture time, level of detail, registration quality and tier (7.8), and a license reference, and MAY carry a validity window and a `supersedes` reference to an older representation it replaces. The registration tier (7.8) applies to exterior representations as it does to interior ones: a survey-grade facade scan is metric, a photogrammetric city tileset is typically navigational, and a device SHOULD prefer the highest-tier representation available for localization and surface the tier when a lower one is used. A representation SHALL NOT be a proxy: it attaches geometry; it does not derive pose. A consumer resolving an entity's representations SHALL, absent a request for history, select the current one by validity and capture time.

> **/req/core/identified-as**
> An `identified_as` relation records an identifier for the entity in an external registry (a parcel number, an asset tag, an IFC GlobalId, a CityGML id, a scan vendor's model id, a tileset feature id, a place id). It SHALL carry the registry name and the identifier. Ingestion of external data SHALL resolve through `identified_as` before minting, so one place never receives two identities because two vendors named it.

Containment and attachment are expressed by the tree, not by relations. The relation graph is what planners and AI reason over; the tree is what renderers and controllers compose. A facility with a parcel record, an IFC model, three LiDAR scans, a panorama capture, and an exterior tileset is one identity with several `identified_as` and several `represents` relations.

## 8. Alignment

> **/req/core/dggs-variant**
> Implementations SHALL declare each DGGS variant they support; records SHALL identify their variant. Where two variants or two resolutions meet, the receiver SHALL coerce to the coarser resolution (13.6) and emit a loss-of-precision indicator.

> **/req/core/geopose**
> Each 4D-State pose SHALL be expressible as GeoPose 1.0: Basic-Quaternion relative to a local tangent plane, Advanced relative to an arbitrary parent.

Informative. The motion and history extensions convert losslessly to OGC Moving Features. 3D Tiles tilesets and content are entities whose tile-local geometry lives in an LCS. The LCS hierarchy carries the semantics of ROS tf2 (latched statics, time-indexed lookups, bounded extrapolation) across the wide area; VDA 5050 AGV state maps onto a 4D-State with the `motion` extension; the ETSI Local Dynamic Map's permanent, transient, and dynamic layers map onto almanac and ephemeris (16.1). OpenXR and glTF bindings are proposed in Annex B.

---

## Annex A (normative). Tests for `core`

| Test | Method | Purpose |
|---|---|---|
| `/conf/core/strict-tree` | F | Register an entity with two parents; expect rejection. |
| `/conf/core/depth` | I, F | Verify declared maximum of at least 12; build to the maximum; attempt one more; expect rejection. |
| `/conf/core/identity-stable` | F | Move, re-measure, restructure, and re-observe an entity across 1,000 records and a loss of contact; verify unchanged 4D-ID. |
| `/conf/core/genesis-anchor` | D | Move an entity across cells; verify identifier unchanged and state anchor updated. |
| `/conf/core/descriptor` | I, D | Verify descriptor form and entropy source. |
| `/conf/core/genesis-implicit` | D | Verify UUIDv7 identifiers normalize and compare equal to explicit form; verify genesis required otherwise. |
| `/conf/core/uri-form` | D | Round-trip through the grammar; verify byte-wise equality. |
| `/conf/core/state-fields` | D | Validate mandatory fields on emitted records. |
| `/conf/core/timestamps` | D | Verify source and publish times and bound on emission; verify receive time not forwarded. |
| `/conf/core/sequence` | F | Inject reordered and missing records; verify detection. |
| `/conf/core/motion-mode` | F | Verify one declared mode; attempt a mode change; expect rejection. |
| `/conf/core/discontinuity` | F | Teleport an entity; verify marker and discarded predictions. |
| `/conf/core/vertical-reference` | D, F | Verify floor index, label, and elevation declared; resolve a floor reference with a horizontal position to a 3D pose. |
| `/conf/core/lcs` | F | Create an LCS straddling cells; verify coarser containing cell; grow it; verify migration as structural history with unchanged identity. |
| `/conf/core/composition` | F | Compare cached global poses to a chain walk over 10,000 entities; move a parent with 10,000 children; verify correct poses and no cache through the moving parent. |
| `/conf/core/uniform-scale` | F | Compose through a 1:1000 embedding; verify scaling of velocity and covariance; verify shear rejected. |
| `/conf/core/uncertainty` | D | Validate covariance layout and confidence range. |
| `/conf/core/provenance` | D | Validate provenance fields; for a fused state, validate supporting observations, fusion authority and model, identity and state confidence. |
| `/conf/core/lifecycle` | F | Take an entity through lost_contact and back; verify records accepted on return; drive it to terminal by authenticated termination; verify subsequent records rejected. |
| `/conf/core/structural-history` | F | Add a wing to a building; verify same 4D-ID, generation increment, history event. |
| `/conf/core/derivation` | F | Fork an entity; verify new 4D-ID with derivation; verify prior resolvable. |
| `/conf/core/labels` | D, F | Add and change labels; verify identity and `identified_as` unaffected. |
| `/conf/core/promotion` | F | Submit agent-generated content directly as Earth-domain state; verify refusal; promote with authority; verify acceptance and provenance. |
| `/conf/core/relation` | D, F | Validate type, validity, confidence, provenance; add relations forming a cycle; verify composition and cycle detection unaffected. |
| `/conf/core/represents` | D, F | Attach a splat and a BIM model to one unit; validate kind, capture time, LOD, registration, tier, license; supersede one; verify the current one is selected absent a history request; verify neither alters the unit's pose. |
| `/conf/core/identified-as` | F | Ingest the same facility from two registries; verify one identity with two `identified_as` relations. |
| `/conf/core/dggs-variant` | F | Exchange records at two resolutions; verify coercion and indicator. |
| `/conf/core/geopose` | D | Convert an LCS pose to GeoPose Basic and back; verify identity to 1e-9 relative. |

## Annex B (informative). Bindings

The access operations of Clause 10 are one semantic API with many bindings. None of the bindings below is normative.

### B.1 Khronos OpenXR
**Proposed `XR_EXT_spatial_entity_4did`.** `xrGet4DIDForSpatialEntityEXT` returns (minting if needed) the 4D-ID of a runtime spatial entity or anchor. `xrCreateSpaceFrom4DIDEXT` resolves a 4D-ID to an `XrSpace`. `xrGet4DStateEXT` returns the 4D-State for a space at a predicted display time. The runtime's reference space is an LCS whose parent is the nearest anchored 4D-ID; because of 5.3 the axis mapping is identity.

### B.2 Khronos glTF
**Proposed `EXT_4did_anchor`.** A node-level extension carrying `id`, `parent`, `anchorTransform` (16 floats, column-major, node to parent LCS), `motionMode`, and `registration`. A scene-level anchor with unanchored children implies LCS-local children. 3D Tiles tilesets carry the same object at tileset and content level.

### B.3 Model Context Protocol
The stateless MCP core routes each request on its own headers, returns cache hints on list and resource reads, and recommends explicit handles returned by tools and passed back as arguments over transport-hidden state. A 4D-ID and a snapshot id are such handles. Mapping: `4did:` identifiers are MCP resources; the Clause 10 operations are tools with JSON Schema inputs and outputs; long-running work (ingesting a scan, registering a reconstruction, generating a scenario domain) uses MCP Tasks; the context envelope (10.6) is the default tool result for an entity. MCP carries context, discovery, queries, and actions. It does not carry the 4D-State stream (13); robots, headsets, vehicles, and renderers stay on that path.

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
  "provenance": { "method": "lidar-slam", "rms_m": 0.011, "registered": "2026-09-04T17:20:00Z" },
  "ext": { "motion": { "velocity": [0.8, 0, -0.2], "confidence": 0.91 } } }
```

## Annex D (informative). Design rationale

Twelve decisions a reviewer is likely to contest, with the alternative rejected and the reason.

1. **Identity layer, not coordinate system.** Alternative: a unified frame. Every domain keeps its native frame; a new one is a sixth silo. What none of them has is a stable name.
2. **DGGS root.** Alternative: raw WGS 84 or a proprietary tiling. A cell is a name, a partition key, a routing key, a query predicate, and a level of detail at once; continuous coordinates are none of those.
3. **Strict tree.** Alternative: DAGs or weighted multi-anchor. Trees bound traversal, make composition unique, and cover every concrete driver today; multi-anchor disagreement resolution has no adequate specification.
4. **Genesis anchor in the identifier, current anchor in state.** Alternative: identifier changes with cell, or carries no spatial part. Stability and currency are different requirements, and a fixed genesis anchor gives every identity a home zone (14.1).
5. **Identity follows continuity, not structure.** Alternative: mint on structural change. A building that gains a wing is the same building; a bridge is the same bridge across a decade of retrofits; an aircraft out of contact for hours is the same aircraft. Structure is history; only a break in continuity (fork, split, merge, replacement) is a new identity.
6. **Three timestamps with a bound.** Alternative: one timestamp or mandated synchronization. Planetary clock skew is unbounded in practice; carrying the bound turns drift into a number.
7. **Motion mode as stable metadata.** Interpolation rules must be known before the first record arrives.
8. **One fixed axis mapping.** Alternative: declared per implementation. Graphics is +Y up, geospatial is ENU, and ambiguity between them is the most common shared-reality defect.
9. **Cache through static ancestors only.** Alternative: cache everything with push invalidation. A moving ship with ten thousand containers would invalidate ten thousand caches per update.
10. **Availability over consistency on partition** (13.4). A vehicle in a tunnel and a robot in a basement keep operating; staleness is marked, never hidden.
11. **Signed attestations, not a ledger** (9.3). Proof of presence needs a signature, not consensus.
12. **Representations share identity; they are not joined into one model.** Alternative: reproject every capture into one continuous space. Captures differ in time, resolution, accuracy, vendor, and license, and forcing them together reconciles errors that do not want to reconcile. Sharing identity and transitioning between representations (Clause 18) is honest, cheap, and fluid; a joined model is none of the three.
13. **Privacy and security as requirements** (Part 3). A pose stream with history and prediction is a surveillance system unless the standard says otherwise, and the substrate is the only layer positioned to enforce the rule across applications.

## Annex E (informative). Change history

| Version | Change |
|---|---|
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
