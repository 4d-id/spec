# 4D-ID Specification

**One persistent name for everything real.** An open standard for spatial identity.

[![License: OGC / Apache-2.0](https://img.shields.io/badge/license-open-blue.svg)](#license)
[![Status: Working Draft](https://img.shields.io/badge/status-working%20draft%202.3-green.svg)](#status)
[![Try it live](https://img.shields.io/badge/try-x4d--id.exe.xyz-4dd0c4.svg)](https://x4d-id.exe.xyz/)

4D-ID gives every object, surface, agent, and environment, physical or virtual, one persistent identity that survives movement, re-observation, vendor boundaries, and the boundary between real and virtual. It is an identity and addressing layer over the standards the world already uses (OGC GeoPose and DGGS, ISO 8601, OpenXR, glTF), not a new coordinate system.

The web gave every document a name that worked across every browser and server. 4D-ID does the same for the physical world.

> **Identities are shared and global, but what you can see and say about them is yours.**

## This repository

This is the **specification**: the authoritative, versioned contract. It is written to be adopted by a neutral standards body (an OGC Standards Working Group is the intended path, with a Khronos liaison for the OpenXR and glTF bindings).

| Path | What it is |
|---|---|
| [`parts/`](parts/) | The specification, in six parts. Part 1 (Core) stands alone. |
| [`schemas/`](schemas/) | JSON Schema 2020-12 for every record type. |
| [`openapi/`](openapi/) | OpenAPI 3.1 description of the access operations (Clause 10). |
| [`conformance/`](conformance/) | The conformance manifest: every test the standard defines. |
| [`CHANGELOG.md`](CHANGELOG.md) | Notable changes per version. |
| [`GOVERNANCE.md`](GOVERNANCE.md) | How the standard is governed and its path to a standards body. |

The **reference implementation** (a resolver you can run in an afternoon), the **SDKs**, and the **conformance CLI** live in sibling repositories:

- [`reference-resolver`](https://github.com/4d-id/reference-resolver) — the resolver, Apache-2.0
- [`js-sdk`](https://github.com/4d-id/js-sdk) — the TypeScript / JavaScript client
- [`demos`](https://github.com/4d-id/demos) — interactive browser demos, also live at [x4d-id.exe.xyz](https://x4d-id.exe.xyz/)

## Read it

Start with **[Part 1: Core](parts/part1-core.md)**. It is about thirteen pages and defines the whole model on four concepts: identity, hierarchy, pose, time. Every later part is optional.

| Part | Read it if you |
|---|---|
| [1 Core](parts/part1-core.md) | implement anything; it stands alone |
| [2 Extensions and access](parts/part2-extensions-and-queries.md) | carry motion, history, attestation, or semantics; serve queries or agents |
| [3 Privacy and security](parts/part3-privacy-and-security.md) | track people, resolve across zones, or serve static content |
| [4 Planetary-scale architecture](parts/part4-planetary-scale-architecture.md) | run more than one zone or authority, or mint identities from perception |
| [5 Domains and presentation](parts/part5-domains-and-presentation.md) | connect simulation or generated environments to the real world |
| [6 Implementation guide](parts/part6-implementation-guide.md) | build one, and want to know which technique makes each rule cheap |

## The one rule of what is normative

A requirement is in the standard only if two independent implementations would fail to interoperate without it. About a hundred requirements survive that rule, each with a test. Everything else is guidance in Part 6.

## Try it before you read it

An interactive resolver, an address-to-identity globe, and animated demos (a robot and drone in a named building; a ship of named containers) run at **[x4d-id.exe.xyz](https://x4d-id.exe.xyz/)**.

## Status

Working Draft 2.3. Not yet adopted by any standards body. Offered for community review. See [GOVERNANCE.md](GOVERNANCE.md) for the intended path.

## Contributing

Review the draft and open an issue or a change request. See [CONTRIBUTING.md](CONTRIBUTING.md). The specification evolves through documented, reviewable change.

## License

The specification text is offered under an open documentation license pending standards-body adoption. The reference implementation, SDKs, schemas, and conformance suite are licensed **Apache-2.0**. See [LICENSE](LICENSE).

The identifier is self-minting and permissionless by design: anyone may create a valid 4D-ID with no registry and no gatekeeper. The standard is intended to be royalty-free.
