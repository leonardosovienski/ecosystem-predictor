"""A minimal PluginV1-compliant reference implementation, used only by the
test suite to prove the registry's discovery/dispatch mechanism against a
real installed entry point (not a hand-rolled mock of the registry's own
internals). No real domain repository is imported here, matching the
"no checkout imports another" rule - this fixture is intentionally
throwaway and lives only in this test tree.
"""

from __future__ import annotations

from ecosystem.contracts import CapabilityManifest, HealthReport, OperationalStatus


class ReferencePlugin:
    domain = "reference"

    def health(self) -> HealthReport:
        return HealthReport(domain=self.domain, status=OperationalStatus.SUCCEEDED, version="0.0.1")

    def capabilities(self) -> CapabilityManifest:
        return CapabilityManifest(domain=self.domain, supports_prediction=True)

    def predict(self, payload: dict) -> dict:
        return {"echo": payload}


class BrokenPlugin:
    """Deliberately non-compliant (no capabilities()) to exercise the
    registry's degraded-load path."""

    domain = "broken"

    def health(self) -> HealthReport:
        return HealthReport(domain=self.domain, status=OperationalStatus.SUCCEEDED)


class AttributeShapedPlugin:
    """Mirrors lol-predictor's real, current shape: `capabilities` is a
    plain attribute, not a method - see docs/adr/0001-plugin-protocol-v1.md.
    Must be rejected at load time, not only when actually called."""

    domain = "attribute-shaped"
    capabilities = ("prediction", "health")

    def health(self) -> HealthReport:
        return HealthReport(domain=self.domain, status=OperationalStatus.SUCCEEDED)
