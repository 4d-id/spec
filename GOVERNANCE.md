# Governance

4D-ID is an open standard. This document describes how it is governed today and the path intended for it.

## Principles

1. **Permissionless.** A 4D-ID is self-minting from a discrete global grid cell and a unique descriptor. There is no central registry, no gatekeeper, and no toll. This property is non-negotiable and will be preserved through any governance transition.
2. **Royalty-free.** The specification is intended to be adopted on royalty-free terms. Implementers may build and ship without a fee.
3. **Compose, do not replace.** 4D-ID builds on existing standards (OGC GeoPose, OGC DGGS, ISO 8601, Khronos OpenXR and glTF) and does not compete with them.
4. **Conformance has teeth.** "4D-ID compliant" means passing the published conformance suite, independent of any single implementation.

## Current stage

The specification is a working draft maintained in this repository by its editors. Changes are proposed as issues and pull requests, reviewed in the open, and recorded in `CHANGELOG.md`. Version numbers follow the specification, not any implementation.

## Intended path

The specification is written to be contributed to a neutral standards body. The intended path is:

- an **OGC Standards Working Group** for the core Implementation Standard, building on GeoPose and DGGS;
- a **Khronos liaison** for the OpenXR and glTF bindings;
- liaison with the **robotics and automated-driving communities** (ROS 2, VDA 5050, ETSI ITS) for the transform-tree and fleet bindings.

Contribution to a neutral body is a deliberate, one-way step taken to make the standard universal. It will be taken when the draft is stable and has independent implementations, and it will preserve the permissionless and royalty-free properties above.

## Decision making

Until the standard is under a standards body, decisions are made by the editors based on documented rationale (see Part 1, Annex D) and community feedback. Substantive changes require an issue describing the problem, a proposed change, and a rationale consistent with the one-rule test: a requirement is normative only if two independent implementations would fail to interoperate without it.
