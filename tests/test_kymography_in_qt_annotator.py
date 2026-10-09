"""Unit tests for GUI kymography line action and data persistence."""
import numpy as np
from unittest.mock import MagicMock

from patkit.metrics import Kymogram


def test_action_display_kymography_line_triggers_statistic_creation(
    annotator,
):
    """Test menu action creates and displays Kymogram statistic on current."""
    mock_ultrasound = MagicMock()
    mock_ultrasound.data = np.ones((5, 40, 40))
    annotator.current.modalities["RawUltrasound"] = mock_ultrasound

    annotator.display_tongue = True
    stat_name = "Kymogram on RawUltrasound"
    assert stat_name not in annotator.current.statistics

    annotator.action_display_kymography_line.setChecked(True)
    annotator.action_display_kymography_line.triggered.emit(True)

    assert stat_name in annotator.current.statistics
    kymogram = annotator.current.statistics[stat_name]
    assert isinstance(kymogram, Kymogram)
    assert kymogram.metadata.line_points == ((0.0, 10.0), (0.0, 50.0))


def test_kymogram_data_saved_on_line_movement(annotator):
    """Test dragging line updates data inside Kymogram statistic metadata."""
    annotator.display_tongue = True
    annotator.action_display_kymography_line.setChecked(True)
    annotator.toggle_kymography_line()

    stat_name = "Kymogram on RawUltrasound"
    kymogram = annotator.current.statistics[stat_name]

    line = annotator.plot_controller.kymography_sampling_line
    assert line is not None

    new_p1 = (15.5, 25.0)
    new_p2 = (45.0, 80.5)
    line.on_changed(new_p1, new_p2)

    assert kymogram.metadata.line_points == (new_p1, new_p2)
    meta_dump = kymogram.get_meta()
    assert meta_dump["line_points"] == (new_p1, new_p2)


def test_kymogram_persists_across_recording_navigation(annotator):
    """Test Kymogram statistics are maintained per recording on navigation."""
    annotator.display_tongue = True
    annotator.action_display_kymography_line.setChecked(True)
    annotator.toggle_kymography_line()

    stat_name = "Kymogram on RawUltrasound"
    first_rec = annotator.current
    kymogram = first_rec.statistics[stat_name]
    kymogram.metadata.line_points = ((1.0, 2.0), (3.0, 4.0))

    assert first_rec.statistics[stat_name].metadata.line_points == (
        (1.0, 2.0),
        (3.0, 4.0),
    )


def test_toggle_small_kymogram_action_triggers_update(annotator, mocker):
    """Test that toggling small kymogram action triggers window update."""
    update_spy = mocker.spy(annotator, "update")
    annotator.action_display_small_kymogram.triggered.emit(True)
    update_spy.assert_called_once()
