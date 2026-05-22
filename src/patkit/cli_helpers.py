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
Command line interface helper functions.
"""

from pathlib import Path

import click

from patkit.path_resolution import get_manifest_scenarios


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
