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
from pydantic import PositiveInt

from patkit.data_structures import (
    AbstractDataContainer, FileInformation, Modality, Statistic,
    StatisticMetaData
)

from .extract_kymogram import extract_kymogram

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
        coordinates ((x1, y1), (x2, y2)).
    num_samples : PositiveInt | None
        Number of points to sample along line segment, by default None.
    """
    parent_name: str
    # TODO 0.23.0: name the end points a and b to make understanding code and
    # saved data easier.
    line_points: tuple[tuple[float, float], tuple[float, float]] = (
        (0.0, 0.0),
        (1.0, 1.0),
    )
    num_samples: PositiveInt | None = None


# TODO 0.23.0: Kymogram is really a metric not a statistic and should have a
# timevector.
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
        num_samples: int | None = None,
    ) -> dict[str, KymogramParameters]:
        """
        Generate Kymogram names and metadata.

        Parameters
        ----------
        parent : Modality | Statistic | str
            Parent Modality, Statistic, or name string.
        line_points : tuple[tuple[float, float], tuple[float, float]]
            Two points in data coordinates defining the line segment.
        num_samples : int | None
            Number of points to sample along line segment, by default None.

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
            num_samples=num_samples,
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
            Sampled kymogram array of shape (num_frames, num_samples).
        """
        parent_name = self.metadata.parent_name
        parent_modality = self.container.modalities[parent_name]
        parent_data = parent_modality.interpolated_frames()

        if parent_data.ndim == 2:
            parent_data = parent_data[np.newaxis, :, :]

        num_frames, height, width = parent_data.shape
        (x1, y1), (x2, y2) = self.metadata.line_points
        num_samples = self.metadata.num_samples

        # Convert data coordinates ((x1, y1), (x2, y2)) to pixel coordinates
        col1 = x1 + width / 2.0
        col2 = x2 + width / 2.0
        row1 = y1
        row2 = y2

        start_point = (col1, row1)
        end_point = (col2, row2)

        # Transpose parent_data from (time, height/row, width/col) to (time,
        # width/col, height/row) so axis 1 is x (col) and axis 2 is y (row)
        video_array = np.transpose(a=parent_data, axes=(0, 2, 1))

        sampled_data = extract_kymogram(
            video_array=video_array,
            start_point=start_point,
            end_point=end_point,
            num_samples=num_samples,
        )

        # TODO 0.23.0: This maybe incorrect
        if num_samples is None and self._data is not None:
            self.metadata.num_samples = self._data.shape[0]

        self._data = sampled_data
        return sampled_data

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
