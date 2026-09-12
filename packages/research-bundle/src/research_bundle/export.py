"""Producer-neutral pinned-source mechanics; admission lists stay in producers."""

import io
import os
import re
import subprocess
from pathlib import Path

from research_bundle import canonical, digest, endpoint, seal, sha, validate
from research_bundle.files import fsync_dir, no_links, safe_mkdirs, safe_open, transfer


def admitted_sources(root, expected, allowed):
    root = no_links(root)
    if type(expected) is not dict or not expected or not set(expected) <= set(allowed):
        raise ValueError("SOURCE_NOT_ADMITTED")
    for value in expected.values():
        sha(value)
    revision = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    sources = {}
    for name, expected_sha in sorted(expected.items()):
        subprocess.run(
            ["git", "-C", str(root), "ls-files", "--error-unmatch", "--", name],
            check=True,
            capture_output=True,
        )
        if subprocess.check_output(["git", "-C", str(root), "status", "--porcelain", "--", name]):
            raise ValueError("SOURCE_NOT_COMMITTED")
        with safe_open(root, name) as source:
            buffer = io.BytesIO()
            transfer(source, buffer, limit=100_000, expected_sha=expected_sha)
            raw = buffer.getvalue()
        # Defense in depth for admitted reports: fail without logging matched data.
        if re.search(
            rb"(?i)(?:api[_-]?key|secret[_-]?key|access[_-]?token|password)[\"']?"
            rb"\s*[:=]\s*[\"']?[A-Za-z0-9_/-]{8,}|-----BEGIN .*PRIVATE KEY-----|"
            rb"(?:sk-proj-|sk_live_)[A-Za-z0-9]+",
            raw,
        ):
            raise ValueError("SENSITIVE_CONTENT")
        raw.decode("utf-8")
        sources[name] = raw
    return revision, sources


class Builder:
    def __init__(self, domain, revision, exporter_revision, expected, exported_at):
        self.body = dict(
            contract="ResearchBundleV1",
            profile="local-research/1",
            origin=dict(
                domain=domain,
                repository="https://github.com/leonardosovienski/"
                + ("cripto" if domain == "crypto" else domain)
                + "-predictor",
                publisher=domain + "-local",
                stream="research-bundle",
                code_revision=revision,
                exporter_revision=exporter_revision,
                inputs=expected,
            ),
            exported_at=exported_at,
            coverage=dict(
                scope="Explicitly admitted existing research metadata",
                completeness="partial",
                included=sorted(expected),
                missing=[],
                excluded=["Protected cohorts", "All other source files and databases"],
                limitations=[
                    "No experiment re-executed",
                    "No scientific or profit validation",
                    "Unknown clocks remain null",
                ],
            ),
            restrictions=dict(
                policy=domain + "-research-bundle/1", read=True, disclose=False, generate=False
            ),
            entities=[],
            evidence=[],
            artifacts=[],
            relations=[],
        )
        self.received = {}

    def entity(
        self,
        identity,
        kind,
        status,
        payload,
        source,
        *,
        axis="scientific",
        identity_basis="source_assigned",
        recorded_at=None,
        event_at=None,
        available_at=None,
    ):
        evidence_id = digest(canonical([source, identity, payload]))
        self.body["evidence"].append(dict(id=evidence_id, source=source, locator=identity, payload=payload))
        entity = dict(
            entity_id=identity,
            entity_type=kind,
            identity_basis=identity_basis,
            status=status,
            status_axis=axis,
            event_at=event_at,
            recorded_at=recorded_at,
            available_at=available_at,
            payload=payload,
            supersedes=[],
            evidence_ids=[evidence_id],
        )
        entity["revision"] = digest(canonical(entity))
        self.body["entities"].append(entity)
        return endpoint("entity", self.body["origin"], identity, entity["revision"])

    def resource(
        self,
        identity,
        locator,
        *,
        raw=None,
        known_sha=None,
        size=None,
        role="document",
        media_type="application/json",
        metadata=None,
    ):
        received = raw is not None
        relative = "files/" + digest(identity.encode()) if received else None
        item = dict(
            artifact_id=identity,
            role=role,
            availability="received" if received else "reference_only",
            media_type=media_type,
            sha256=digest(raw) if received else known_sha,
            size=len(raw) if received else size,
            relative_path=relative,
            locator=locator,
            logical_name=identity,
            metadata=metadata or {},
        )
        self.body["artifacts"].append(item)
        if received:
            self.received[relative] = raw
        return endpoint("artifact", self.body["origin"], identity)

    def relation(self, source, kind, target):
        body = dict(type=kind, source=source, target=target)
        self.body["relations"].append(dict(relation_id=digest(canonical(body)), **body))

    def publish(self, root, destination, sources):
        root = Path(root).absolute()
        destination = Path(destination).absolute()
        if destination.is_relative_to(root) or not destination.is_relative_to(root.parent):
            raise ValueError("OUTPUT_OUTSIDE_PRODUCER_EXPORT_AREA")
        package = validate(seal(self.body))
        # Verify every pinned source again, before creating any output.
        for name, raw in sources.items():
            with safe_open(root, name) as source:
                transfer(source, limit=100_000, expected_sha=digest(raw), expected_size=len(raw))
        safe_mkdirs(destination.parent)
        destination.mkdir(exist_ok=False)
        for relative, raw in self.received.items():
            target = destination / relative
            target.parent.mkdir(exist_ok=True)
            with target.open("xb") as out:
                out.write(raw)
                out.flush()
                os.fsync(out.fileno())
            fsync_dir(target.parent)
        # Completion manifest is last: interrupted exports are not bundles.
        with (destination / "bundle.json").open("xb") as out:
            out.write(canonical(package))
            out.flush()
            os.fsync(out.fileno())
        fsync_dir(destination)
        return package
