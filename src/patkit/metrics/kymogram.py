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
Kymogram Statistic and its Parameter class.
"""

import logging

import numpy as np

from patkit.data_structures import (
    AbstractDataContainer, FileInformation, Modality, Statistic,
    StatisticMetaData
)

_logger = logging.getLogger('patkit.kymogram')


class KymogramParameters(StatisticMetaData):
    """
    Parameters used in defining a Kymogram statistic.

    Parameters
    ----------
    parent_name : str
        Name of the Modality or Statistic this instance of Kymogram was
        calculated on or defined for.
    line_points : tuple[tuple[float, float], tuple[float, float]]
        Coordinates of the kymography sampling line as two points in data
        coordinates ((x1, y1), (x2, y2)), defaults to None when not set.
    """
    parent_name: str
    line_points: tuple[tuple[float, float], tuple[float, float]] | None = None


class Kymogram(Statistic):
    """
    Kymogram statistic representing a 2D sampling along a line over time.
    """

    @classmethod
    def generate_name(cls, params: KymogramParameters) -> str:
        """
        Generate a Kymogram name to be used as its unique identifier.

        Parameters
        ----------
        params : KymogramParameters
            The parameters of the Kymogram instance.

        Returns
        -------
        str
            Name of the Kymogram instance.
        """
        return f"{cls.__name__} on {params.parent_name}"

    @staticmethod
    def get_names_and_meta(
        parent: Modality | Statistic | str,
        line_points: tuple[
            tuple[float, float], tuple[float, float]
        ] = ((0.0, 0.0), (1.0, 1.0)),
    ) -> dict[str, KymogramParameters]:
        """
        Generate Kymogram names and metadata.

        Parameters
        ----------
        parent : Modality | Statistic | str
            Parent Modality, Statistic, or name string.
        line_points : tuple[tuple[float, float], tuple[float, float]]
            Two points in data coordinates defining the line segment.

        Returns
        -------
        dict[str, KymogramParameters]
            Dictionary mapping generated name to metadata instance.
        """
        if isinstance(parent, str):
            parent_name = parent
        elif isinstance(parent, (Statistic, Modality)):
            parent_name = parent.__class__.__name__
        else:
            parent_name = parent.__name__

        params = KymogramParameters(
            parent_name=parent_name,
            line_points=line_points,
        )
        return {Kymogram.generate_name(params=params): params}

    def __init__(
        self,
        container: AbstractDataContainer,
        metadata: KymogramParameters,
        file_info: FileInformation,
        parsed_data: np.ndarray | None = None,
    ) -> None:
        """
        Build a Kymogram instance.

        Parameters
        ----------
        container : AbstractDataContainer
            Containing Session or Recording.
        metadata : KymogramParameters
            Parameters defining this instance of Kymogram.
        file_info : FileInformation
            FileInformation metadata for this Kymogram.
        parsed_data : np.ndarray | None, optional
            The sampled kymogram array, by default None.
        """
        super().__init__(
            container=container,
            metadata=metadata,
            file_info=file_info,
            parsed_data=parsed_data,
        )

    def _derive_data(self) -> np.ndarray:
        """
        Calculate the kymogram sampled data from the parent modality.

        Returns
        -------
        np.ndarray
            Sampled kymogram array.
        """
        raise NotImplementedError(
            "Kymogram sampling computation will be implemented in Step 4."
        )

    def get_meta(self) -> dict:
        """
        Get metadata as a dictionary.

        Returns
        -------
        dict
            The metadata dictionary.
        """
        return self.metadata.model_dump()

    @property
    def name(self) -> str:
        """
        Unique name identifier of the Kymogram.

        Returns
        -------
        str
            Generated Kymogram name.
        """
        return Kymogram.generate_name(params=self.metadata)
