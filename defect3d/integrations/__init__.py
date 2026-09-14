"""Integration registry and adapter boundary for the BlackMamba 3D ecosystem."""

from .registry import (
    PROVIDERS,
    Provider,
    all_capabilities,
    capability_matrix,
    ecosystem_summary,
    get_provider,
    missing_capabilities,
    providers_for,
)

__all__ = [
    "PROVIDERS",
    "Provider",
    "all_capabilities",
    "capability_matrix",
    "ecosystem_summary",
    "get_provider",
    "missing_capabilities",
    "providers_for",
]
