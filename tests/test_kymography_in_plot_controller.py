"""Unit tests for PlotController kymography line integration."""

from unittest.mock import MagicMock

from patkit.metrics import Kymogram, KymogramParameters
from patkit.data_structures import FileInformation


def test_toggle_kymography_line_creates_statistic(
    plot_controller, dummy_recording
):
    """Test that toggling line creates Kymogram statistic if missing."""
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
    assert plot_controller.kymography_sampling_line is not None
    assert plot_controller.kymography_sampling_line.get_visible() is True


def test_toggle_kymography_line_switching_recordings(
    plot_controller, dummy_recording
):
    """Test updating line endpoints when switching recordings."""
    plot_controller.ultra_axes = MagicMock()
    plot_controller.ultra_canvas = MagicMock()

    # Initial call creates line with default points ((0.0, 10.0), (0.0, 50.0))
    plot_controller.toggle_kymography_line(
        recording=dummy_recording,
        visible=True,
    )

    # Create a second recording with custom Kymogram line points
    second_params = KymogramParameters(
        parent_name="RawUltrasound",
        line_points=((5.0, 15.0), (25.0, 35.0)),
    )
    second_recording = MagicMock()
    second_recording.statistics = {
        "Kymogram on RawUltrasound": Kymogram(
            container=second_recording,
            metadata=second_params,
            file_info=FileInformation(),
        )
    }

    # Toggle with second recording
    plot_controller.toggle_kymography_line(
        recording=second_recording,
        visible=True,
    )

    line = plot_controller.kymography_sampling_line
    assert line.get_coordinates() == ((5.0, 15.0), (25.0, 35.0))


def test_kymography_line_drag_updates_recording_statistic(
    plot_controller, dummy_recording
):
    """Test that line movement updates statistic line_points metadata."""
    plot_controller.ultra_axes = MagicMock()
    plot_controller.ultra_canvas = MagicMock()

    plot_controller.toggle_kymography_line(
        recording=dummy_recording,
        visible=True,
    )

    line = plot_controller.kymography_sampling_line
    kymogram = dummy_recording.statistics["Kymogram on RawUltrasound"]

    # Simulate line change callback triggered by a drag event
    line.on_changed((12.0, 34.0), (56.0, 78.0))

    assert kymogram.metadata.line_points == ((12.0, 34.0), (56.0, 78.0))


def test_toggle_kymography_line_visibility(plot_controller, dummy_recording):
    """Test toggling visibility state of kymography sampling line."""
    plot_controller.ultra_axes = MagicMock()
    plot_controller.ultra_canvas = MagicMock()

    # Explicitly set visible=True
    plot_controller.toggle_kymography_line(
        recording=dummy_recording,
        visible=True,
    )
    line = plot_controller.kymography_sampling_line
    assert line.get_visible() is True

    # Toggle visibility without specifying visible parameter (None toggles)
    plot_controller.toggle_kymography_line(
        recording=dummy_recording,
        visible=None,
    )
    assert line.get_visible() is False

    # Explicitly set visible=True again
    plot_controller.toggle_kymography_line(
        recording=dummy_recording,
        visible=True,
    )
    assert line.get_visible() is True
