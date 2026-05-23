"""
Tests for path resolution logic.

This module checks whether file and directory paths are accurately
resolved to their corresponding Patkit OpenPathType.
"""
from pathlib import Path

import pytest

from patkit.constants import OpenPathType, PatkitConfigFile, SourceSuffix
from patkit.path_resolution import resolve_open_path


def test_resolve_open_path_manifest(tmp_path: Path) -> None:
    """
    Test resolving a path to a manifest file or directory containing it.

    Parameters
    ----------
    tmp_path : Path
        Pytest fixture providing a temporary directory.
    """
    # Test directory containing a manifest
    manifest_file = tmp_path / PatkitConfigFile.MANIFEST
    manifest_file.touch()

    # When passing the directory
    path_type, target = resolve_open_path(path=tmp_path)
    assert path_type == OpenPathType.MANIFEST
    assert target == manifest_file

    # When passing the manifest file directly
    path_type, target = resolve_open_path(path=manifest_file)
    assert path_type == OpenPathType.MANIFEST
    assert target == manifest_file


def test_resolve_open_path_scenario(tmp_path: Path) -> None:
    """
    Test resolving a path to a scenario configuration file or directory.

    Parameters
    ----------
    tmp_path : Path
        Pytest fixture providing a temporary directory.
    """
    # Test directory containing a data config (making it a scenario)
    config_file = tmp_path / PatkitConfigFile.DATA
    config_file.touch()

    # When passing the directory
    path_type, target = resolve_open_path(path=tmp_path)
    assert path_type == OpenPathType.SCENARIO
    assert target == tmp_path

    # When passing the config file directly
    path_type, target = resolve_open_path(path=config_file)
    assert path_type == OpenPathType.SCENARIO
    # It should correctly resolve back to the parent directory
    assert target == tmp_path


def test_resolve_open_path_single_data(tmp_path: Path) -> None:
    """
    Test resolving a path to a single data file.

    Parameters
    ----------
    tmp_path : Path
        Pytest fixture providing a temporary directory.
    """
    # Test a single data file
    data_file = tmp_path / f"test_recording{SourceSuffix.WAV}"
    data_file.touch()

    path_type, target = resolve_open_path(path=data_file)
    assert path_type == OpenPathType.SINGLE_DATA
    assert target == data_file


def test_resolve_open_path_directory(tmp_path: Path) -> None:
    """
    Test resolving a path to an empty directory.

    Parameters
    ----------
    tmp_path : Path
        Pytest fixture providing a temporary directory.
    """
    # Test an empty directory (no config or manifest)
    path_type, target = resolve_open_path(path=tmp_path)
    assert path_type == OpenPathType.DIRECTORY
    assert target == tmp_path


def test_resolve_open_path_invalid_file(tmp_path: Path) -> None:
    """
    Test that an invalid file extension raises a ValueError.

    Parameters
    ----------
    tmp_path : Path
        Pytest fixture providing a temporary directory.
    """
    # .txt is a valid AAA_PROMPT, so we must use an unknown extension
    # like .xyz
    bad_file = tmp_path / "random_file.xyz"
    bad_file.touch()

    with pytest.raises(
        expected_exception=ValueError,
        match="not a recognized PATKIT configuration",
    ):
        resolve_open_path(path=bad_file)
