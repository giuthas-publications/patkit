"""Unit tests for plot_kymogram in patkit.plot_and_publish."""

from unittest.mock import MagicMock

import numpy as np

from patkit.plot_and_publish.plot import plot_kymogram


def test_plot_kymogram_renders_axes_image():
    """Test that plot_kymogram clears axes and returns AxesImage."""
    axes = MagicMock()
    kymogram_data = np.zeros((10, 20))

    image = plot_kymogram(
        axes=axes,
        kymogram_data=kymogram_data,
        current_frame_index=3,
        cmap="gray",
    )

    axes.clear.assert_called_once()
    axes.imshow.assert_called_once()
    axes.axvline.assert_called_once_with(
        x=3,
        color="red",
        linewidth=1,
        linestyle="--",
    )
    assert image is not None


def test_plot_kymogram_without_current_frame_index():
    """Test plot_kymogram without drawing selected frame indicator line."""
    axes = MagicMock()
    kymogram_data = np.zeros((10, 20))

    plot_kymogram(
        axes=axes,
        kymogram_data=kymogram_data,
        current_frame_index=None,
        cmap="gray",
    )

    axes.clear.assert_called_once()
    axes.imshow.assert_called_once()
    axes.axvline.assert_not_called()