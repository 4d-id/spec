# Governance

4D-ID 2.4, dated November 3, 2026, is a working draft offered for community review; no standards body has adopted it. This document describes how the draft is governed today and possible future paths.

## Principles

1. **Permissionless generation, governed resolution.** The identifier format may be generated without a central registry, gatekeeper, or toll. Conforming resolution is existing-identity-first: an acceptable existing identity SHALL be reused; minting is permitted only after a bounded, completed, scoped and unexpired no-acceptable-match decision, subject to resolver and authority rules. Incomplete or exhausted lookup is not no-match.
2. **Royalty-free.** The draft is designed for royalty-free publication and licensing; this is not an adoption claim. Implementers may build and ship without a fee.
3. **Compose, do not replace.** 4D-ID builds on existing standards (OGC GeoPose, OGC DGGS, ISO 8601, Khronos OpenXR and glTF) and does not compete with them. Grounding determines the referent, localization determines where it is, and 4D-ID preserves which resolved referent continues across systems and time.
4. **Conformance has teeth.** A conformance claim names the version, profile, classes, declared policies, and evidence for all applicable normative tests. The 2.4 manifest defines 112 tests; wired partial schema checks are not full functional conformance, and `todo` is not a pass. No implementation compliance or standards-body adoption is asserted by publishing these artifacts.

## Current stage

This working draft is maintained in this repository by its editors. Changes are proposed as issues and pull requests, reviewed in the open, and recorded in `CHANGELOG.md`. Version numbers follow the specification, not any implementation.

## Review scope for 2.4 and 2.5

Version 2.4 preserves one composition parent while recording many external registrations, separates identity from spatial indexing without reminting legacy IDs, and makes bounded reconciliation and authority disputes explicit. Authority fields record attribution; authentication, authorization, precedence, and grant verification remain declared deployment policy under the normative security requirements. Editors do not adjudicate legal ownership of named referents.

The larger identifier/grid design remains open for 2.5. Review should compare non-spatial home-token discovery, privacy and linkability, migration continuity, and grid-independent routing. Any decision needs documented rationale and interoperability tests; this draft does not preselect a standards-body outcome.

## Possible future path

The draft is prepared for community review and possible future submission to neutral standards bodies. Possible liaison targets include:

- an **OGC Standards Working Group** for the core Implementation Standard, building on GeoPose and DGGS;
- a **Khronos liaison** for the OpenXR and glTF bindings;
- liaison with the **robotics and automated-driving communities** (ROS 2, VDA 5050, ETSI ITS) for the transform-tree and fleet bindings.

Editors may submit a stable draft for consideration when it has independent implementations. Any submission is a reviewable decision, not a one-way adoption step, and would preserve the permissionless generation and royalty-free properties above.

## Decision making

Until this working draft is submitted to a standards body, decisions are made by the editors based on documented rationale (see Part 1, Annex D) and community feedback. Substantive changes require an issue describing the problem, a proposed change, and a rationale consistent with the one-rule test: a requirement is normative only if two independent implementations would fail to interoperate without it.
