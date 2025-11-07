#
# Copyright (c) 2019-2025
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
Calculate and add Intensity to a Recording.
"""

import logging

import numpy as np

from patkit.data_structures import Modality, Recording

from .intensity import Intensity

_logger = logging.getLogger('patkit.intensity')


def calculate_intensity(parent_modality: Modality) -> np.ndarray:
    """
    Calculate overall intensity on the Modality as a function of time.

    Parameters
    ----------
    parent_modality : Modality
        Modality containing grayscale data.

    Returns
    -------
    np.ndarray
        Overall intensity as a function of time.
    """
    data = parent_modality.data
    return np.sum(data, axis=(1, 2))


def add_intensity(
    recording: Recording,
    modality: Modality,
    preload: bool = True,
    release_data_memory: bool = False,
) -> None:
    """
    Calculate Intensity and add it to the Recording.

    Parameters
    ----------
    recording : Recording
        The Recording the new Intensity will be added to.
    modality : Modality
        The Modality the new Intensity will be calculated on.
    preload : bool, optional
        Should the Intensity be calculated on creation (preloaded) or only on
        access, by default True
    release_data_memory : bool, optional
        Should the data attribute of the Modality be set to None after use, by
        default True

    Raises
    ------
    NotImplementedError
        Running with preload set to False has not yet been implemented.
    """
    if not preload:
        message = ("Looks like somebody is trying to leave Intensity to be "
                   "calculated on the fly. This is not yet supported.")
        raise NotImplementedError(message)

    if recording.excluded:
        _logger.info(
            "Recording %s excluded from processing.", recording.basename)
    elif not modality.__name__ in recording:
        _logger.info("Data modality '%s' not found in recording: %s.",
                     modality.__name__, recording.basename)
    else:
        all_requested = Intensity.get_names_and_meta(
            modality, release_data_memory)
        missing_keys = set(all_requested).difference(
            recording.keys())
        to_be_computed = dict((key, value) for key,
                              value in all_requested.items()
                              if key in missing_keys)

        data_modality = recording[modality.__name__]

        if to_be_computed:
            # intensities = calculate_intensity(data_modality, to_be_computed)
            intensities = calculate_intensity(data_modality)

            for intensity in intensities:
                recording.add_modality(intensity)
                _logger.info("Added '%s' to recording: %s.",
                             intensity.name, recording.basename)
        else:
            _logger.info(
                "Nothing to compute in Intensity for Recording: %s.",
                recording.basename)
