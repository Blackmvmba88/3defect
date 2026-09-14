"""Integration registry and adapter boundary for the BlackMamba 3D ecosystem."""

from .adapter import AdapterResult, IntegrationAdapter, adapter_supports
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
from .workspace import missing_repositories, repository_folder, scan_workspace

__all__ = [
    "AdapterResult",
    "IntegrationAdapter",
    "PROVIDERS",
    "Provider",
    "adapter_supports",
    "all_capabilities",
    "capability_matrix",
    "ecosystem_summary",
    "get_provider",
    "missing_capabilities",
    "missing_repositories",
    "providers_for",
    "repository_folder",
    "scan_workspace",
]
