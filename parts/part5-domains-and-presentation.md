# 4D-ID 2.3, Part 5: Domains, portals, proxies, and presentation

**Unified Spatiotemporal Identity for Shared Reality. Candidate Open Standard Working Draft, Part 5 of 6.**

| | |
|---|---|
| Editors | D. Lorenzini and N. Lorenzini, Quantum Studio |
| Version | 2.3 (working draft) |
| Date | September 2026 |
| Status | Candidate open standard working draft, offered for community review. Not adopted by any standards body. |

## Abstract

Simulators, generated environments, HD-map builds, game instances, and any space not on Earth have no DGGS cell. This Part gives them roots (domains), joins frames without breaking the tree (portals), lets a thing in one frame stand for a thing in another (proxies), and makes re-theming a proxy rather than a copy (views). Physical truth governs collision; authority never flows from virtual to physical; disclosure is inherited, never widened.

## Conformance

This Part defines the requirements classes `domain` (Clause 17) and `presentation` (Clause 18). Conformance, profiles, normative references, terms, and conventions are in Part 1. Numbering is unique across the family (Part 1, 5.5). `domain` requires `lifecycle` and, where human-associated entities are proxied, `privacy` and `security` 12.3; `presentation` requires only `core`.

---

## 17. Domains, portals, proxies, and views (requirements class: `domain`)

Part 1 assumes every identity is minted in a DGGS cell. Simulators, generated environments, HD-map builds, game instances, and any space not on Earth have no cell. This clause removes the assumption with four constructs built from primitives the core already has.

### 17.1 Domains

A domain is a root frame with its own grid. Earth is the domain whose grid is DGGS. A domain root is an entity: it has a 4D-ID, a home zone, a lifecycle, and optionally a parent.

> **/req/domain/declaration**
> A domain SHALL declare its grid (a DGGS variant for Earth; `oct` or a documented synthetic grid otherwise), a mode (**real**, **replica** of a real place, **scenario** proposing changes to a real place, or **generated**), an extent policy (fixed or growing), a time mapping (17.5), an instance relation (template or instance of a template), provenance (generating model and version, source capture or prompt; for a domain derived from a real place, a `derived_from` reference to the Earth anchor with an externally supplied registration transform and quality), and its authority. Source capture/prompt and registration transform/quality are supplied by external generators or registration services; the family records them.

> **/req/domain/embedding**
> A domain root MAY have a parent in another domain. An embedded domain is an ordinary node whose transform MAY carry uniform scale (7.7) and which counts toward depth (7.1). Within a domain space SHALL be Euclidean; non-Euclidean connectivity SHALL be expressed only through portals. A generated environment whose geometry does not close on itself SHALL be modeled as several domains joined by portals.

> **/req/domain/instancing**
> An instance of a template domain SHALL share the template's almanac by content address and SHALL carry its own dynamic state, zones, and generations. A free-standing virtual domain SHALL carry a lease; when it expires, every entity rooted in it SHALL move to terminal in one operation (lease expiry is an authoritative termination, 7.9).

A robot fleet's training simulation, the HD-map build a vehicle validates against, a proposed modification to a facility, and a generated environment a headset user walks through are domains of the same kind, distinguished by mode. A scenario domain SHALL carry a `derived_from` reference to the real anchor it proposes to change; consumers SHALL be able to distinguish a scenario from the record without inspecting content.

### 17.2 Portals

> **/req/domain/portal**
> A portal SHALL consist of two aperture entities, each with pose and extent in its own frame, and a signed link (12.2) carrying the transform from aperture A local to aperture B local (rigid plus optional uniform scale), direction, a see-through flag, a traversal policy over layers and credentials, and a lease. Portals SHALL be held in a graph distinct from the parent tree and SHALL NOT participate in composition, traversal, depth, or cycle detection; queries MAY consult them (10.2, 10.3).

> **/req/domain/portal-crossing**
> An entity crossing a portal SHALL be re-parented: same 4D-ID, new parent, pose rewritten through the portal transform, and a discontinuity marker referencing the portal. Consumers holding the transform MAY interpolate through the aperture.

An AGV entering a delivery vehicle, a robot boarding an elevator, and an avatar stepping into a generated room are all portal crossings: the frame changes, the identity does not.

### 17.3 Proxies

A proxy is an entity in one frame whose pose is derived from a source in another. An entity has one parent and any number of proxies. A real robot appears in its simulation as a proxy; a virtual obstacle appears to a real robot as a proxy; a hologram on a real desk is a proxy of the virtual object.

> **/req/domain/proxy**
> A proxy SHALL carry its own 4D-ID, a `proxy_of` reference to exactly one source, a binding (identity, fixed offset, portal, or documented function), and authority delegated to the source's authority. Its pose SHALL be recomputed whenever the source publishes, and it SHALL inherit the source's lifecycle, confidence, and decay.

> **/req/domain/authority-asymmetry**
> Authority flows from physical to virtual. No virtual domain, layer, or proxy SHALL hold authority over the pose of an entity rooted in the Earth domain. Commands to physical actuators are not 4D-States and are out of scope.

> **/req/domain/affordance-truth**
> For a proxy co-located with its source in the Earth domain, the source hull (9.4) SHALL govern collision, occlusion, and navigation. The proxy's interactable hull SHALL contain the source hull and MAY exceed it only with a divergence flag consumers SHALL surface.

A person's body is an Earth entity: it never crosses a portal and never leaves Clause 11. Their avatar is a proxy that does. Disclosure is inherited, never widened (12.3).

### 17.4 Views

A view is a layer whose entities are identity-bound proxies of another layer's entities, presented with different assets by a client. Re-theming a room, showing pipe routes through a wall, or overlaying a planned layout on a live warehouse are views.

> **/req/domain/view-identity**
> Interaction in a view (ray-cast hits, selection, hand-offs) SHALL reference the source 4D-ID through `proxy_of`, not the view's asset. Two consumers in different views of one space SHALL resolve one physical object to one identity.

Appearance is out of scope; the asset a view binds to a class is an opaque reference. Licensing of assets and styles is a deployment matter.

### 17.5 Domain time

> **/req/domain/time-mapping**
> Source, publish, and receive times remain wall-clock in every domain. A domain SHALL declare domain time as a piecewise-linear function of wall time whose rate MAY be zero (paused) or negative (replay). History and prediction queries SHALL accept either clock. While rate is zero, consumers SHALL NOT extrapolate.

A simulation running at ten times real time, a replay of yesterday's shift, and a paused generated scene each declare a mapping; retention (11.3) is enforced in wall time regardless.

### 17.6 Correspondence

> **/req/domain/correspondence**
> An external correspondence/matching or registration service MAY submit a `corresponds_to` relation (7.9) between entities in different domains, carrying an externally computed transform estimate in addition to its confidence. Consumers MAY use the recorded result for relocalization or registration. This family does not determine correspondence, relocalize, or register. Entities in different domains SHALL NOT be merged (15.2).


---

## 18. Presentation (requirements class: `presentation`)

Moving a viewer from a regional view to a site to an interior scan is not flight through one continuous model. It is resolving one identity down its hierarchy and handing off between representations captured separately, at different fidelity, under different licenses. This clause carries what a client needs to make that handoff fast and continuous. It adds no geometry and performs no registration; it names identifiers, placement inputs, and continuity metadata for clients, not rendering or computed registration.

### 18.1 Viewpoints

> **/req/presentation/viewpoint**
> A viewpoint SHALL be an entity carrying a pose and a `frames` relation to the entity it is composed to show. A client MAY place a camera at a viewpoint to render the framed entity. Viewpoints travel with the identity they frame, so any client renders the same vantage.

An approach view of a facility, an entry, and a per-space vantage are viewpoints on the facility, the floor, and the spaces.

### 18.2 Level-of-detail ladder

> **/req/presentation/ladder**
> An entity MAY declare a level-of-detail ladder: an ordered list of (level, entity) pairs naming the representation or child to show at each scale, coarsest to finest. A client MAY build a transition sequence by walking the ladder. The ladder is a convenience over the tree and `represents` relations (7.9) and SHALL NOT contradict them.

Region to site to building to floor to space is one ladder; a client flies it by walking the rungs.

### 18.3 Transitions and continuity

> **/req/presentation/transition**
> A transition hint MAY be declared between two representations or two rungs of a ladder. It SHALL carry the pair, a trigger (a distance or angular-size threshold, or an explicit user action), and a **continuity anchor**: the 4D-ID of the entity a client SHALL keep fixed across the transition. On transition, the client SHALL place the outgoing and incoming cameras relative to the continuity anchor's pose in each representation, so the anchor holds the same screen position across the cut.

The continuity anchor is what makes a fade feel like passing through the thing rather than jumping to another view. A selection of a loading door on a facade, with that door as the anchor, lands the interior camera on the same door the exterior camera was looking at, because the door is one identity with one pose in each representation. The visual treatment (fade, match cut, dolly) is out of scope; the anchor and the camera placement are not.

### 18.4 Registration tier and presentation

> **/req/presentation/tier-honesty**
> A client using a representation for navigation or transition MAY use a logical or navigational registration (7.8). A client presenting a measurement, a fit, or any survey-relevant result SHALL use a metric registration and SHALL indicate when a shown representation is below metric tier.

Navigational placement is enough to move through a building; it is not enough to tell a contractor a wall will fit.

### 18.5 Overlay confidence

A client that draws content onto the viewer's live view of the real world (a highlight on a structure the viewer is looking at, a label on a distant feature) depends on two uncertainties: how well the viewer's own pose is known, and how well the target entity is registered.

> **/req/presentation/overlay-confidence**
> A client/localizer compositing an overlay onto the real world SHALL combine the viewer's localization uncertainty (7.8) with the target entity's registration uncertainty into a combined placement uncertainty, and SHALL degrade the overlay (fading, widening, outlining, or suppressing) as that uncertainty grows, so that a confidently placed overlay and a poorly placed one are visually distinct. A confidently drawn overlay on the wrong target is a failure this requirement exists to prevent.

At 80 meters a half-degree pose error moves an overlay a meter, onto the neighboring feature. Combining the two uncertainties, and showing the result, is what keeps a highlight honest: solid when the placement is trustworthy, tentative when it is not.
---

## Annex A (normative). Tests for Part 5

| Test | Method | Purpose |
|---|---|---|
| `/conf/domain/declaration` | D, F | Verify grid, mode, extent policy, time mapping, instance relation, provenance, authority; verify a scenario domain carries `derived_from` and is distinguishable from a real one by mode alone. |
| `/conf/domain/embedding` | F | Embed a domain at 1:1000; verify depth accounting and composition; submit an externally registered non-closing loop result and verify refusal or split. |
| `/conf/domain/instancing` | F | Instance a template twice; verify shared almanac and independent state; expire a domain; verify descendants terminal. |
| `/conf/domain/portal` | F | Add a portal; verify composition, depth, and cycle detection unaffected; verify one-signature portal refused. |
| `/conf/domain/portal-crossing` | F | Cross a portal; verify re-parent, transformed pose, portal-referenced marker. |
| `/conf/domain/proxy` | F | Move a source; verify proxy pose and lifecycle follow within the validity window; rebind without source authority; verify refusal. |
| `/conf/domain/authority-asymmetry` | F | Submit an Earth-entity pose from a virtual domain's authority; verify rejection. |
| `/conf/domain/affordance-truth` | F | Bind a smaller proxy hull to a real obstacle; verify rejection or divergence flag. |
| `/conf/domain/view-identity` | F | Ray-cast from two views; verify the same source 4D-ID. |
| `/conf/domain/time-mapping` | F | Pause a domain; verify extrapolation suspended; query history in both clocks. |
| `/conf/domain/correspondence` | F | Submit externally computed correspondence and verify it is recorded and consumable; verify cross-domain merge is refused and no in-family matcher or registration step is required. |
| `/conf/presentation/viewpoint` | D, F | Place a viewpoint; verify a client consumes its identifiers and placement inputs to compose the framed entity. |
| `/conf/presentation/ladder` | D | Validate an ordered LOD ladder; verify it agrees with the tree and `represents`. |
| `/conf/presentation/transition` | F | Declare a transition with a door as continuity anchor; verify the anchor holds screen position across the cut. |
| `/conf/presentation/tier-honesty` | F | Present a sub-metric representation for measurement; verify the tier is indicated and metric required. |
| `/conf/presentation/overlay-confidence` | F | A client composites a target at range with poor viewer localization; verify the overlay degrades and does not present as confident. |

*End of Part 5.*
