from pathlib import Path

from patkit.constants import PatkitConfigFile
from patkit.data_structures import Manifest


def get_manifest_scenarios(path: Path) -> list[Path] | None:
    """
    Find and resolve all scenario paths from a manifest.

    Parameters
    ----------
    path : Path
        The original target path provided by the user.

    Returns
    -------
    list[Path] | None
        A list of resolved, absolute paths found in the manifest if a non-empty
        manifest was found. Returns None if no manifest was found or an empty
        list if it is empty.
    """
    if path.is_file() and path.suffix == PatkitConfigFile.MANIFEST:
        manifest_path = path
    elif path.is_dir():
        manifest_path = path / PatkitConfigFile.MANIFEST
        if not manifest_path.is_file():
            return
    else:
        return None

    manifest = Manifest(path=manifest_path)

    resolved_paths = []
    for scenario in manifest:
        scenario_path = Path(scenario)
        if not scenario_path.is_absolute():
            scenario_path = (manifest_path.parent / scenario_path).resolve()

        resolved_paths.append(scenario_path)

    return resolved_paths
