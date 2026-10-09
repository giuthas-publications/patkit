"""Unit tests for PlotController kymography line integration."""

import numpy as np
from unittest.mock import MagicMock

from patkit.metrics import Kymogram, KymogramParameters
from patkit.data_structures import FileInformation


def test_draw_kymogram_renders_small_kymogram(
    plot_controller, dummy_recording
):
    """Test that draw_kymogram populates kymogram_axes when checked."""
    mock_ultrasound = MagicMock()
    mock_ultrasound.data = np.ones((5, 40, 40))
    dummy_recording.modalities["RawUltrasound"] = mock_ultrasound

    params = KymogramParameters(
        parent_name="RawUltrasound",
        line_points=((0.0, 10.0), (0.0, 50.0)),
    )
    kymogram = Kymogram(
        container=dummy_recording,
        metadata=params,
        file_info=FileInformation(),
        parsed_data=np.ones((5, 20)),
    )
    dummy_recording.statistics["Kymogram on RawUltrasound"] = kymogram

    plot_controller.kymogram_axes = MagicMock()
    plot_controller.kymogram_canvas = MagicMock()
    plot_controller.main_window.action_display_small_kymogram.isChecked = (
        MagicMock(return_value=True)
    )

    result = plot_controller.draw_kymogram(recording=dummy_recording)

    assert result is True
    plot_controller.kymogram_axes.imshow.assert_called_once()
    plot_controller.kymogram_canvas.draw_idle.assert_called_once()


def test_draw_kymogram_skipped_when_action_unchecked(
    plot_controller, dummy_recording
):
    """Test that draw_kymogram clears canvas if display action is unchecked."""
    mock_ultrasound = MagicMock()
    mock_ultrasound.data = np.ones((5, 40, 40))
    dummy_recording.modalities["RawUltrasound"] = mock_ultrasound

    plot_controller.kymogram_axes = MagicMock()
    plot_controller.kymogram_canvas = MagicMock()
    plot_controller.main_window.action_display_small_kymogram.isChecked = (
        MagicMock(return_value=False)
    )

    result = plot_controller.draw_kymogram(recording=dummy_recording)

    assert result is False
    plot_controller.kymogram_axes.clear.assert_called_once()
    plot_controller.kymogram_canvas.draw_idle.assert_called_once()


"""Unit tests for PlotController kymography line integration."""


def test_toggle_kymography_line_creates_statistic(
    plot_controller, dummy_recording
):
    """Test that toggling line creates Kymogram statistic if missing."""
    mock_ultrasound = MagicMock()
    mock_ultrasound.data = np.ones((5, 40, 40))
    dummy_recording.modalities["RawUltrasound"] = mock_ultrasound

    assert "Kymogram on RawUltrasound" not in dummy_recording.statistics

    plot_controller.ultra_axes = MagicMock()
    plot_controller.ultra_canvas = MagicMock()

    plot_controller.toggle_kymography_line(
        recording=dummy_recording,
        visible=True,
    )

    stat_name = "Kymogram on RawUltrasound"
    assert stat_name in dummy_recording.statistics
    kymogram = dummy_recording.statistics[stat_name]
    assert kymogram.metadata.line_points == ((0.0, 10.0), (0.0, 50.0))
    # Data remains None until adjusted by user
    assert kymogram.data is None
    assert plot_controller.kymography_sampling_line is not None
    assert plot_controller.kymography_sampling_line.get_visible() is True


def test_kymography_line_drag_populates_data_and_renders(
    plot_controller, dummy_recording
):
    """Test that line movement derives data and triggers kymogram draw."""
    mock_ultrasound = MagicMock()
    mock_ultrasound.data = np.ones((5, 40, 40))
    dummy_recording.modalities["RawUltrasound"] = mock_ultrasound

    plot_controller.ultra_axes = MagicMock()
    plot_controller.ultra_canvas = MagicMock()
    plot_controller.kymogram_axes = MagicMock()
    plot_controller.kymogram_canvas = MagicMock()
    plot_controller.main_window.action_display_small_kymogram.isChecked = (
        MagicMock(return_value=True)
    )

    plot_controller.toggle_kymography_line(
        recording=dummy_recording,
        visible=True,
    )

    line = plot_controller.kymography_sampling_line
    kymogram = dummy_recording.statistics["Kymogram on RawUltrasound"]
    assert kymogram.data is None

    # Drag sampling line
    line.on_changed((12.0, 34.0), (56.0, 78.0))

    assert kymogram.metadata.line_points == ((12.0, 34.0), (56.0, 78.0))
    assert kymogram.data is not None
    plot_controller.kymogram_axes.imshow.assert_called_once()


def test_draw_kymogram_uninitialized_returns_false(
    plot_controller, dummy_recording
):
    """
    Test that draw_kymogram clears canvas and returns False when data is None.
    """
    mock_ultrasound = MagicMock()
    mock_ultrasound.data = np.ones((5, 40, 40))
    dummy_recording.modalities["RawUltrasound"] = mock_ultrasound

    plot_controller.kymogram_axes = MagicMock()
    plot_controller.kymogram_canvas = MagicMock()
    plot_controller.main_window.action_display_small_kymogram.isChecked = (
        MagicMock(return_value=True)
    )

    params = KymogramParameters(
        parent_name="RawUltrasound",
        line_points=((0.0, 10.0), (0.0, 50.0)),
    )
    kymogram = Kymogram(
        container=dummy_recording,
        metadata=params,
        file_info=FileInformation(),
    )
    dummy_recording.statistics["Kymogram on RawUltrasound"] = kymogram

    result = plot_controller.draw_kymogram(recording=dummy_recording)

    assert result is False
    plot_controller.kymogram_axes.clear.assert_called_once()
    plot_controller.kymogram_canvas.draw_idle.assert_called_once()


def test_draw_kymogram_renders_when_data_exists(
    plot_controller, dummy_recording
):
    """Test that draw_kymogram renders when kymogram data is populated."""
    mock_ultrasound = MagicMock()
    mock_ultrasound.data = np.ones((5, 40, 40))
    dummy_recording.modalities["RawUltrasound"] = mock_ultrasound

    plot_controller.kymogram_axes = MagicMock()
    plot_controller.kymogram_canvas = MagicMock()
    plot_controller.main_window.action_display_small_kymogram.isChecked = (
        MagicMock(return_value=True)
    )

    params = KymogramParameters(
        parent_name="RawUltrasound",
        line_points=((0.0, 10.0), (0.0, 50.0)),
    )
    kymogram = Kymogram(
        container=dummy_recording,
        metadata=params,
        file_info=FileInformation(),
        parsed_data=np.ones((5, 20)),
    )
    dummy_recording.statistics["Kymogram on RawUltrasound"] = kymogram

    result = plot_controller.draw_kymogram(recording=dummy_recording)

    assert result is True
    plot_controller.kymogram_axes.imshow.assert_called_once()
    plot_controller.kymogram_canvas.draw_idle.assert_called_once()
