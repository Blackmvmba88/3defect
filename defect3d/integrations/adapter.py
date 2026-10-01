"""Stable adapter boundary for external BlackMamba 3D providers.

Adapters are intentionally tiny. They translate the canonical Mamba3D contract
to/from one provider without letting provider-specific paths or APIs leak into
the core orchestration layer.
"""

from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Sequence, Tuple


@dataclass(frozen=True)
class AdapterResult:
    """Normalized result returned by any ecosystem adapter."""

    provider: str
    operation: str
    success: bool
    artifacts: Tuple[str, ...] = ()
    measurements: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)
    errors: Tuple[str, ...] = ()


class IntegrationAdapter(Protocol):
    """Protocol every executable repository bridge must implement."""

    key: str
    capabilities: Sequence[str]

    def health(self) -> Mapping[str, Any]:
        """Return availability/version information without mutating anything."""

    def execute(
        self,
        operation: str,
        asset: Mapping[str, Any],
        workspace: str,
    ) -> AdapterResult:
        """Execute one provider-specific operation against the canonical asset."""


def adapter_supports(adapter: IntegrationAdapter, capability: str) -> bool:
    """Return True when an adapter advertises a capability."""
    return capability in adapter.capabilities
