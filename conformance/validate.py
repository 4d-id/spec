#!/usr/bin/env python3
"""Validate 2.4 specification artifacts and partial shape fixtures, never runtime conformance."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path
import re
from urllib.parse import unquote, urldefrag, urljoin

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from openapi_spec_validator import validate as validate_openapi
from referencing import Registry, Resource

from shape_checks import BASE, DECISION, EXTRA_CHECKS, ID, SCHEMA_CHECKS

ROOT = Path(__file__).resolve().parents[1]
NEW_TESTS = {
    "/conf/core/genesis-privacy", "/conf/core/reconciliation",
    "/conf/fabric/conferred-authority", "/conf/fabric/overlapping-authority",
    "/conf/fabric/dispute",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate key: {key}")
        result[key] = value
    return result


def load_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_pairs)


class UniqueLoader(yaml.SafeLoader):
    pass


def yaml_mapping(loader, node):
    return unique_pairs((loader.construct_object(k), loader.construct_object(v)) for k, v in node.value)


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, yaml_mapping)


def linkage(manifest):
    require(manifest["version"] == "2.4" and manifest["date"] == "2026-11-03", "Manifest version/date drift")
    require(manifest["encoding"] == "../encoding/2.4.md", "Missing versioned encoding pointer")
    requirements, annex = {}, {}
    parts = sorted((ROOT / "parts").glob("part*.md"))
    require(len(parts) == 6, "Expected six parts")
    for part in parts:
        text = part.read_text()
        require("2.4, Part" in text.splitlines()[0], f"Wrong title: {part}")
        require("| Version | 2.4 (working draft) |" in text, f"Wrong version: {part}")
        require("| Date | November 3, 2026 |" in text, f"Wrong date: {part}")
        require("| Status | Working draft offered for community review." in text, f"Wrong status: {part}")
        for match in re.finditer(r"^> \*\*(/req/[a-z0-9-]+/[a-z0-9-]+)\*\*\n(> .+(?:\n> .+)*)", text, re.M):
            key, body = match.groups()
            require(key not in requirements, f"Duplicate requirement {key}")
            require(re.search(r"\b(SHALL|SHOULD|MAY)\b", body), f"Requirement without normative keyword: {key}")
            requirements[key] = part.name
        for key, method in re.findall(r"^\| `(/conf/[a-z0-9-]+/[a-z0-9-]+)` \| ([IDF, ]+) \|", text, re.M):
            require(key not in annex, f"Duplicate Annex A test {key}")
            annex[key] = (part.name, set(method.replace(",", "").replace(" ", "")))
    tests = manifest["tests"]
    ids = [test["id"] for test in tests]
    require(len(ids) == 112 and len(set(ids)) == 112, "Manifest must have exactly 112 unique normative tests")
    require(len(requirements) == len(annex) == 112, "Expected 112 requirement blocks and 112 Annex A tests")
    require(set(ids) == set(annex), "Manifest/Annex A ID mismatch")
    require({key.replace("/req/", "/conf/") for key in requirements} == set(ids), "Requirement/test linkage mismatch")
    require(NEW_TESTS <= set(ids), "Missing 2.4 additions")
    require(len(set(ids) - NEW_TESTS) == 107, "Expected 107 existing tests plus five additions")
    wired = set()
    for test in tests:
        key = test["id"]
        req = key.replace("/conf/", "/req/")
        require(test["requirement"] == req, f"Incorrect requirement link: {key}")
        require(requirements[req] == annex[key][0], f"Test in wrong Part: {key}")
        require(set(test["method"]) == annex[key][1], f"Method mismatch: {key}")
        require(test["status"] in {"todo", "schema"}, f"Unjustified status: {key}")
        if key in NEW_TESTS:
            require(test["status"] == "todo", f"New normative test must remain todo: {key}")
        if test["status"] == "schema":
            require("D" in test["method"] and test.get("coverage"), f"Missing partial coverage statement: {key}")
            wired.add(key)
    require(wired == set(SCHEMA_CHECKS), "Manifest schema checks must map exactly to executable fixtures")
    print("Linkage: 112 requirements = 112 Annex A tests = 112 manifest entries (107 + 5)")
    print("Normative coverage:", dict(Counter(test["status"] for test in tests)), "; no functional pass claim")


def main():
    manifest = load_json(ROOT / "conformance/manifest.json")
    linkage(manifest)
    docs = {}
    registry = Registry()
    schemas = sorted((ROOT / "schemas").glob("*.json"))
    for path in schemas:
        schema = load_json(path)
        require(schema["$id"] == BASE + path.name, f"Wrong versioned schema ID: {path}")
        require("November 3, 2026" in schema.get("$comment", ""), f"Missing schema date: {path}")
        require(schema["$schema"] == "https://json-schema.org/draft/2020-12/schema", f"Wrong dialect: {path}")
        Draft202012Validator.check_schema(schema)
        docs[path.as_uri()] = docs[schema["$id"]] = schema
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
    api_path = ROOT / "openapi/openapi.yaml"
    api = yaml.load(api_path.read_text(), Loader=UniqueLoader)
    docs[api_path.as_uri()] = api
    require(api["openapi"] == "3.1.0", "Wrong OpenAPI version")
    require(api["info"]["version"] == "2.4" and api["info"]["x-spec-date"] == "2026-11-03", "OpenAPI release drift")
    require(api["info"]["x-status"] == "working draft offered for community review", "OpenAPI maturity drift")
    require(all("/v2.4" in item["url"] for item in api["servers"]), "OpenAPI server version drift")

    def resolve(ref, base):
        uri, fragment = urldefrag(urljoin(base, ref))
        require(uri in docs, f"Missing or non-local reference: {uri}")
        value = docs[uri]
        if fragment:
            require(fragment.startswith("/"), f"Only JSON Pointer references are supported: {ref}")
            for token in unquote(fragment[1:]).split("/"):
                token = token.replace("~1", "/").replace("~0", "~")
                value = value[int(token)] if isinstance(value, list) else value[token]
        # A file reference into a schema still inherits that schema's canonical ID.
        return value, docs[uri].get("$id", uri)

    def check_refs(value, base):
        if isinstance(value, dict):
            base = urljoin(base, value.get("$id", ""))
            if "$ref" in value:
                resolve(value["$ref"], base)
            for child in value.values():
                check_refs(child, base)
        elif isinstance(value, list):
            for child in value:
                check_refs(child, base)

    def materialize(value, base):
        # Offline, fully dereferenced validation copy only. Source artifacts retain
        # their published IDs and relative/versioned references unchanged.
        if isinstance(value, dict):
            base = urljoin(base, value.get("$id", ""))
            result = {}
            if "$ref" in value:
                target, target_base = resolve(value["$ref"], base)
                result.update(materialize(target, target_base))
            result.update({k: materialize(v, base) for k, v in value.items() if k not in {"$ref", "$id"}})
            return result
        if isinstance(value, list):
            return [materialize(child, base) for child in value]
        return value

    for path in schemas:
        check_refs(docs[path.as_uri()], path.as_uri())
    check_refs(api, api_path.as_uri())
    validate_openapi(materialize(api, api_path.as_uri()))
    print(f"Artifacts: {len(schemas)} Draft 2020-12 schemas and OpenAPI 3.1 validate; all references resolve offline")

    count = 0
    for name, cases in SCHEMA_CHECKS.items():
        require({expected for _, expected, _ in cases} == {True, False}, f"Need positive and negative checks: {name}")
    groups = [*SCHEMA_CHECKS.items(), ("additional draft regressions", EXTRA_CHECKS)]
    for name, cases in groups:
        for index, (ref, expected, instance) in enumerate(cases):
            validator = Draft202012Validator({"$ref": ref}, registry=registry, format_checker=FormatChecker())
            errors = list(validator.iter_errors(instance))
            require((not errors) == expected, f"{name} fixture {index}: expected {expected}, errors: {errors}")
            count += 1
    # Test that each HTTP response actually constrains the intended decision outcome.
    response_cases = {"200": ["reuse"], "404": ["no_acceptable_match"], "409": ["ambiguous", "conflict"],
                      "403": ["rejected"], "503": ["ambiguous", "conflict", "rejected"]}
    for status, allowed in response_cases.items():
        schema = api["paths"]["/resolve"]["get"]["responses"][status]["content"]["application/json"]["schema"]
        validator = Draft202012Validator(materialize(schema, api_path.as_uri()), format_checker=FormatChecker())
        for outcome in ("reuse", "no_acceptable_match", "ambiguous", "conflict", "rejected"):
            instance = deepcopy(DECISION)
            instance["outcome"] = outcome
            if outcome == "reuse":
                instance["selected_id"] = ID
            if status == "200":
                instance = {"id": ID, "locator": "zone:1", "snapshot_id": "snapshot:1", "decision": instance}
            require(validator.is_valid(instance) == (outcome in allowed), f"HTTP {status} outcome binding mismatch: {outcome}")
            count += 1
    # Keep the illustrative state in Part 1 parseable and shape-valid too.
    core = (ROOT / "parts/part1-core.md").read_text()
    example = json.loads(re.search(r"## Annex C.*?```json\n(.*?)\n```", core, re.S).group(1))
    Draft202012Validator({"$ref": BASE + "state.json"}, registry=registry, format_checker=FormatChecker()).validate(example)
    print(f"Shape regressions: {count} positive/negative assertions and the Part 1 example passed")
    print("Partial artifact checks only. All five new normative tests remain todo; no runtime code tested.")


if __name__ == "__main__":
    main()
