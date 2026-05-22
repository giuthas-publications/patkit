from pathlib import Path

import click

from patkit.constants import PatkitConfigFile
from patkit.data_structures import Manifest


def resolve_scenario_path(path: Path) -> Path:
    """
    Resolve a potentially ambiguous path to a specific scenario path.

    If the provided path is a directory containing a manifest, or a direct
    path to a manifest file, this function reads the manifest. If multiple
    scenarios are recorded, the user is prompted to select one. If only one
    is found, it is automatically selected. If no manifest is found, the
    original path is returned.

    Parameters
    ----------
    path : Path
        The original target path provided by the user.

    Returns
    -------
    Path
        The resolved path to a specific scenario, or the original path if
        no manifest resolution applies.
    """
    # Determine the manifest path based on whether input is a file or dir
    if path.is_file():
        manifest_path = path
    elif path.is_dir():
        manifest_path = path / PatkitConfigFile.MANIFEST
    else:
        return path

    if manifest_path.is_file():
        try:
            # Manifest handles reading the file during initialization
            manifest = Manifest(path=manifest_path)
            # Use the property defined in the Manifest class
            scenarios = manifest.scenarios
        except Exception:
            scenarios = []

        # Filter out empty paths just in case to avoid broken indices
        scenarios = [s.strip() for s in scenarios if s.strip()]

        if scenarios:
            if len(scenarios) == 1:
                chosen_path = Path(scenarios[0])

                # Resolve relative scenario paths using the manifest's location
                if not chosen_path.is_absolute():
                    chosen_path = (
                        manifest_path.parent / chosen_path
                    ).resolve()

                click.echo(
                    f"Automatically opening the single scenario from "
                    f"manifest: {chosen_path}"
                )
                return chosen_path

            # More than one scenario exists; prompt the user
            click.echo("\nMultiple scenarios found in the manifest file:")
            for idx, s_path in enumerate(scenarios, 1):
                click.echo(f"  [{idx}] {s_path}")

            choice = click.prompt(
                "\nPlease select which scenario you want to open",
                type=click.IntRange(1, len(scenarios)),
                default=1
            )

            chosen_path = Path(scenarios[choice - 1])
            if not chosen_path.is_absolute():
                chosen_path = (manifest_path.parent / chosen_path).resolve()

            click.echo(f"Opening selected scenario: {chosen_path}\n")
            return chosen_path

    # If no valid manifest is found, return the original untouched path
    return path
