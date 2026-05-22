#
# Copyright (c) 2019-2026
# Pertti Palo, Scott Moisik, Matthew Faytak, and Motoki Saito.
#
# This file is part of the Phonetic Analysis ToolKIT
# (see https://github.com/giuthas/patkit/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# The example data packaged with this program is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License. You should have received a
# copy of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License along with the data. If not,
# see <https://creativecommons.org/licenses/by-nc-sa/4.0/> for details.
#
# When using the toolkit for scientific publications, please cite the
# articles listed in README.md. They can also be found in
# citations.bib in BibTeX format.
#
"""
PATKIT command line commands.
"""

from pathlib import Path

import click

from patkit.constants import OpenPathType
from patkit.initialise import initialise_config, initialise_patkit
from patkit.path_resolution import get_manifest_scenarios, resolve_open_path
from patkit.qt_annotator import run_annotator
from patkit.interpreter import run_interpreter
from patkit.simulation import run_simulations
from patkit.simulation.simulate import setup_contours_comparisons_soundpairs


def resolve_scenario_path(path: Path) -> Path:
    """
    CLI-specific path resolution that prompts the user via the terminal.

    Parameters
    ----------
    path : Path
        The original target path provided by the user.

    Returns
    -------
    Path
        The chosen scenario path, or the original path if none apply.
    """
    scenarios = get_manifest_scenarios(path=path)

    if not scenarios:
        return path

    if len(scenarios) == 1:
        click.echo(
            f"Automatically opening the single scenario from "
            f"manifest: {scenarios[0]}"
        )
        return scenarios[0]

    click.echo("\nMultiple scenarios found in the manifest file:")
    for idx, s_path in enumerate(scenarios, 1):
        click.echo(f"  [{idx}] {s_path}")

    choice = click.prompt(
        "\nPlease select which scenario you want to open",
        type=click.IntRange(1, len(scenarios)),
        default=1
    )

    chosen_path = scenarios[choice - 1]
    click.echo(f"Opening selected scenario: {chosen_path}\n")

    return chosen_path


@click.command(name="open")
@click.argument(
    "path",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=True, path_type=Path
    ),
)
def open_in_annotator(
        path: Path
) -> None:
    """
    Open the PATH in the annotator GUI.

    \b
    PATH to the data - maybe be a file or a directory.
    """
    path_type, path = resolve_open_path(path)
    match path_type:
        case OpenPathType.MANIFEST:
            path = resolve_scenario_path(path=path)
        case OpenPathType.SCENARIO:
            pass
        case OpenPathType.DIRECTORY:
            raise NotImplementedError(
                "Opening a directory of data without "
                "config is not implemented yet."
            )
        case OpenPathType.SINGLE_DATA:
            raise NotImplementedError(
                "Opening a single data file without "
                "config is not implemented yet."
            )
        case _:
            raise NotImplementedError(
                f"Unimplemented type of load path "
                f"{path_type}."
            )

    config, logger = initialise_config(
        path=path, require_gui=True, require_data=True)
    session = initialise_patkit(config=config, logger=logger)
    run_annotator(session=session, config=config)


@click.command()
@click.argument(
    "path",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=True, path_type=Path
    ), )
def interact(
        path: Path
):
    """
    Open the PATH in interactive commandline mode.

    \b
    PATH to the data - maybe be a file or a directory.
    """
    path = resolve_scenario_path(path=path)
    config, logger = initialise_config(path=path, require_data=True)
    session = initialise_patkit(config=config, logger=logger)
    run_interpreter(session=session, configuration=config)


@click.command()
@click.argument(
    "path",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=True, path_type=Path
    ), )
def publish(path: Path):
    """
    Publish plots from the data in PATH.

    \b
    PATH to the data - maybe be a file or a directory.

    NOT IMPLEMENTED YET.
    """
    path = resolve_scenario_path(path=path)
    config, logger = initialise_config(path=path, require_publish=True)
    session = initialise_patkit(config=config, logger=logger)
    print(
        f"Loaded {session} but rest of publish is scheduled for "
        f"implementation in a later version."
    )


@click.command()
@click.argument(
    "path",
    type=click.Path(dir_okay=True, file_okay=True, path_type=Path),
)
def simulate(path: Path):
    """
    Run a simulation experiment.

    \b
    PATH to a `.yaml` file which contains the parameters for running the
    simulation.
    """
    # TODO 0.24: simulate command will not work if given the actual config file
    # instead of containing dir
    config, _ = initialise_config(path=path, require_simulation=True)
    contours, comparisons, sound_pairs = setup_contours_comparisons_soundpairs(
        sim_configuration=config.simulation_config)
    run_simulations(
        sim_configuration=config.simulation_config,
        contours=contours,
        comparisons=comparisons,
        sound_pairs=sound_pairs
    )
