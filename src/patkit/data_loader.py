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
Import or load a Session from a directory.
"""

import logging
from pathlib import Path

from patkit.audio_processing import MainsFilter
from patkit.configuration import Configuration, PathStructure
from patkit.constants import (
    DatasourceNames, SourceSuffix, PatkitSuffix, PatkitConfigFile)
from patkit.data_import import (
    generate_aaa_recording_list, load_session_config)
from patkit.data_structures import (
    FileInformation, Session, SessionConfig)
from patkit.save_and_load import load_recording_session

_logger = logging.getLogger('patkit.scripting')

# TODO 1.0: change the name of this file to data_importer and move it to a more
# appropriate submodule.


def load_data(configuration: Configuration) -> Session:
    """
    Handle loading data from individual files or a previously saved session.

    Parameters
    ----------
    configuration : Configuration
        patkit configuration.

    Returns
    -------
    Session
        The generated Session object with the exclusion list applied.
    """
    # TODO 0.18 Should not blindly assume that sampling frequency is 44100!
    path = configuration.data_config.recorded_data_path
    if configuration.data_config.mains_frequency:
        MainsFilter.generate_mains_filter(
            44100,
            configuration.data_config.mains_frequency)
    else:
        print(
            "No mains frequency specified. Guessing 60 Hz. Please "
            "check if this is correct where the data was recorded.")
        MainsFilter.generate_mains_filter(44100, 60)

    meta_files = path.glob("*" + PatkitSuffix.META)
    match len(list(meta_files)):
        case 1:
            session = load_recording_session(path)
        case _:
            session = read_recording_session_from_dir(path)

    for recording in session:
        recording.after_modalities_init()

    return session


def read_recording_session_from_dir(
        recorded_data_path: Path,
        detect_beep: bool = False
) -> Session:
    """
    Wrapper for reading data from a directory full of files.

    Having this as a separate method allows subclasses to change
    arguments or even the parser.

    Note that to make data loading work in a consistent way,
    this method just returns the data and saving it in an
    instance variable is left for the caller to handle.
    """
    containing_dir = recorded_data_path.parts[-1]
    session_config_path = recorded_data_path / PatkitConfigFile.SESSION
    session_meta_path = recorded_data_path / (containing_dir + '.Session' +
                                              PatkitSuffix.META)
    if session_meta_path.is_file():
        session = load_recording_session(
            recorded_data_path, session_config_path
        )
        return session

    file_info = FileInformation(
        recorded_path=recorded_data_path,
        recorded_meta_file=session_config_path.name)
    if session_config_path.is_file():
        paths, session_config = load_session_config(
            recorded_data_path, session_config_path)

        match session_config.data_source_name:
            case DatasourceNames.AAA:
                recordings = generate_aaa_recording_list(
                    directory=recorded_data_path,
                    import_config=session_config)

                session = Session(
                    name=containing_dir, paths=paths, config=session_config,
                    file_info=file_info, recordings=recordings)
                return session
            case DatasourceNames.RASL:
                raise NotImplementedError(
                    "Loading RASL data hasn't been implemented yet.")
            case _:
                raise NotImplementedError(
                    f"Unrecognised data source: "
                    f"{session_config.data_source_name}")

    if list(recorded_data_path.glob('*' + SourceSuffix.AAA_ULTRA)):
        recordings = generate_aaa_recording_list(
            directory=recorded_data_path,
            detect_beep=detect_beep
        )

        paths = PathStructure(root=recorded_data_path)
        session_config = SessionConfig(data_source_name=DatasourceNames.AAA)

        session = Session(
            name=containing_dir, paths=paths, config=session_config,
            file_info=file_info, recordings=recordings)
        return session

    _logger.error(
        'Could not find a suitable importer: %s', recorded_data_path)
