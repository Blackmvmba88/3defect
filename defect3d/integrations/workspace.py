"""Local workspace discovery for BlackMamba 3D provider repositories."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Mapping

from .registry import PROVIDERS


@dataclass(frozen=True)
class RepositoryMount:
    """Expected local mount for one ecosystem provider."""

    provider: str
    repository: str
    path: str
    present: bool
    git_checkout: bool


# Some providers share one repository. The registry remains capability-oriented,
# while workspace scanning deduplicates physical repository checkouts.
def repository_folder(repository: str) -> str:
    """Return the conventional checkout folder for owner/name."""
    return repository.rsplit("/", 1)[-1]


def scan_workspace(root: str) -> List[Mapping[str, object]]:
    """Inspect a parent folder and report expected repository checkouts.

    This function never clones, modifies, fetches or executes a repository.
    It is safe to use as a read-only preflight before wiring adapters.
    """
    base = Path(root).expanduser().resolve()
    seen_repositories = set()
    mounts: List[Mapping[str, object]] = []

    for provider in PROVIDERS:
        if provider.repository in seen_repositories:
            continue
        seen_repositories.add(provider.repository)

        path = base / repository_folder(provider.repository)
        present = path.is_dir()
        mounts.append(
            {
                "repository": provider.repository,
                "path": str(path),
                "present": present,
                "git_checkout": present and (path / ".git").exists(),
                "provider_keys": [
                    item.key
                    for item in PROVIDERS
                    if item.repository == provider.repository
                ],
            }
        )

    return mounts


def missing_repositories(root: str) -> List[str]:
    """Return repository names not found beneath the workspace root."""
    return [
        str(item["repository"])
        for item in scan_workspace(root)
        if not item["present"]
    ]
