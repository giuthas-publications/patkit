from dataclasses import dataclass
from typing import Annotated, Callable

import numpy as np
from pydantic import BaseModel

from patkit.constants import ComparisonMember, SplineMetricEnum, \
    SplineShapesEnum

MetricFunction = Annotated[
    Callable[[np.ndarray], np.ndarray],
    "Metrics need to accept one np.ndarray as argument and "
    "return a np.ndarray. This is only an alias for 'Metric'"
]


class ComparisonSoundPair(BaseModel, frozen=True):
    """
    Defines a comparison between two contours.

    First should be compared to second.
    """
    first: str
    second: str

    def __repr__(self) -> str:
        return (f"Comparison: from first {self.first} "
                f"to second {self.second}.")


class Comparison(ComparisonSoundPair):
    """
    Defines a comparison between two contours, and which of them is perturbed.

    First should be compared to second with the contour named in perturbed
    being the one that gets perturbed.
    """
    # first: str
    # second: str
    perturbed: ComparisonMember

    @property
    def perturbed_name(self) -> str:
        """
        Name of the perturbed contour.

        Returns
        -------
        str
            The name as a string.
        """
        if self.perturbed == ComparisonMember.FIRST:
            return self.first
        return self.second

    def __repr__(self) -> str:
        return (f"Comparison: from first {self.first} "
                f"to second {self.second}, perturbed is {self.perturbed}")


@dataclass
class ShapeMetricSimulationResult:
    """
    Baseline and results from simulations of shape metrics.

    Parameters
    ----------
    metric : SplineShapesEnum
        Metric used in deriving the results.
    baselines : dict[str, float]
        Baseline for each metric and contour.
    results : dict[str, dict[str, np.ndarray]]
        Results for each metric/contour/perturbation
    """
    metric: SplineShapesEnum
    baselines: dict[str, float]
    results: dict[str, dict[str, np.ndarray]]


@dataclass
class DistanceMetricSimulationResult:
    """
    Baseline and results from simulations of shape metrics.

    Parameters
    ----------
    metric : SplineMetricEnum
        Metric used in deriving the results. While SplineMetricEnum includes
        also spline shape metrics, passing one here will result in a ValueError
        being raised or unpredictable behavior.
    baselines : dict[str, float]
        Baseline for each metric and contour.
    results : dict[Comparison, dict[str, np.ndarray]]
        Results for each metric/contour/perturbation
    """
    metric: SplineMetricEnum
    baselines: dict[Comparison, float]
    results: dict[Comparison, dict[str, np.ndarray]]

    def __post_init__(self):
        if isinstance(self.metric, SplineShapesEnum):
            raise ValueError(
                f"DistanceMetricSimulationResult does not accept "
                f"SplineShapesEnum as metric type. Found {self.metric}."
            )
