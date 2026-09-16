"""Tests for local BlackMamba 3D workspace discovery."""

from pathlib import Path

from defect3d.integrations import missing_repositories, repository_folder, scan_workspace


def test_repository_folder_uses_repo_name():
    assert repository_folder("Blackmvmba88/3defect") == "3defect"
    assert repository_folder("Blackmvmba88/XarvisCore") == "XarvisCore"


def test_workspace_scan_detects_present_checkout(tmp_path: Path):
    repo = tmp_path / "3defect"
    repo.mkdir()
    (repo / ".git").mkdir()

    rows = scan_workspace(str(tmp_path))
    core = next(row for row in rows if row["repository"] == "Blackmvmba88/3defect")

    assert core["present"] is True
    assert core["git_checkout"] is True
    assert "core" in core["provider_keys"]


def test_workspace_scan_deduplicates_shared_repository(tmp_path: Path):
    rows = scan_workspace(str(tmp_path))
    repositories = [row["repository"] for row in rows]
    assert len(repositories) == len(set(repositories))


def test_missing_repositories_reports_absent_repos(tmp_path: Path):
    missing = missing_repositories(str(tmp_path))
    assert "Blackmvmba88/3defect" in missing
    assert "Blackmvmba88/weaponassambly" in missing
