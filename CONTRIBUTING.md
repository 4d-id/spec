# Contributing to the 4D-ID Specification

Thank you for helping improve 4D-ID. The standard gets better through review from people who build real spatial systems.

## Ways to contribute

- **Review and comment.** Read the draft (start with `parts/part1-core.md`) and open an issue for anything unclear, wrong, or missing.
- **Propose a change.** Open an issue describing the problem before opening a pull request. Substantive changes need a rationale.
- **Report an interoperability gap.** If two implementations could disagree because the spec is ambiguous, that is a bug in the spec. Tell us where.
- **Contribute a test.** The conformance manifest defines the checks for this candidate draft. Better tests strengthen the proposal; current tooling has 15 schema-level checks passing while functional conformance work continues.

## The one rule

A requirement is normative only if two independent implementations would fail to interoperate without it. Proposals that add requirements need to pass this test; proposals that turn requirements into guidance are welcome where the test fails.

## Process

1. Open an issue describing the problem and, if you have one, a proposed change.
2. Discussion happens in the open, on the issue.
3. Accepted changes land via pull request, update `CHANGELOG.md`, and, where they touch requirements, update the conformance manifest.
4. Editors merge once the change is consistent with the rationale in Part 1, Annex D.

## Style

- Prose, minimal formatting. Requirements are labeled `/req/<class>/<name>` with a matching test `/conf/<class>/<name>`.
- RFC 2119 keywords (SHALL, SHOULD, MAY) only where a requirement is meant.
- Keep examples balanced across domains: robotics, automated driving, geospatial, XR, and AI.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating you agree to uphold it.
