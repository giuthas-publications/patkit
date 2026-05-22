from pathlib import Path

from patkit.constants import PatkitConfigFile
from patkit.data_structures import Manifest


def get_manifest_scenarios(path: Path) -> list[Path]:
    """
    Find and resolve all scenario paths from a manifest.

    This function contains no UI elements and is safe to call from both
    CLI and GUI contexts.

    Parameters
    ----------
    path : Path
        The original target path provided by the user.

    Returns
    -------
    list[Path]
        A list of resolved, absolute paths found in the manifest. Returns
        an empty list if no manifest is found or if it is empty.
    """
    if path.is_file():
        manifest_path = path
    elif path.is_dir():
        manifest_path = path / PatkitConfigFile.MANIFEST
    else:
        return []

    if not manifest_path.is_file():
        return []

    try:
        manifest = Manifest(path=manifest_path)
        raw_scenarios = manifest.scenarios
    except Exception:
        raw_scenarios = []

    # Clean and resolve paths
    resolved_paths: list[Path] = []
    for s in raw_scenarios:
        if not s.strip():
            continue

        scenario_path = Path(s.strip())
        if not scenario_path.is_absolute():
            scenario_path = (manifest_path.parent / scenario_path).resolve()

        resolved_paths.append(scenario_path)

    return resolved_paths
