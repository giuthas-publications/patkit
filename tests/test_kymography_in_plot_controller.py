"""Unit tests for PlotController kymography line integration."""

from unittest.mock import MagicMock

from patkit.metrics import Kymogram


def test_toggle_kymography_line_creates_statistic(
    plot_controller, dummy_recording
):
    """Test that toggling line creates Kymogram statistic if missing."""
    assert "Kymogram on RawUltrasound" not in dummy_recording.statistics

    # Mock ultra_axes and canvas drawing methods
    plot_controller.ultra_axes = MagicMock()
    plot_controller.ultra_canvas = MagicMock()

    plot_controller.toggle_kymography_line(
        recording=dummy_recording,
        visible=True,
    )

    assert "Kymogram on RawUltrasound" in dummy_recording.statistics
    kymogram = dummy_recording.statistics["Kymogram on RawUltrasound"]
    assert isinstance(kymogram, Kymogram)
    assert kymogram.metadata.line_points == ((0.0, 10.0), (0.0, 50.0))


def test_toggle_kymography_line_visibility(plot_controller, dummy_recording):
    """Test toggling visibility state of kymography sampling line."""
    plot_controller.ultra_axes = MagicMock()
    plot_controller.ultra_canvas = MagicMock()

    plot_controller.toggle_kymography_line(
        recording=dummy_recording,
        visible=True,
    )
    line = plot_controller.kymography_sampling_line
    assert line is not None
    assert line.get_visible() is True

    plot_controller.toggle_kymography_line(
        recording=dummy_recording,
        visible=False,
    )
    assert line.get_visible() is False
