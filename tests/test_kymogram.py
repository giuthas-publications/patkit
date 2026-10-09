"""Unit tests for Kymogram statistic and KymogramParameters."""

import pytest

from patkit.data_structures import FileInformation
from patkit.metrics import Kymogram, KymogramParameters


def test_kymogram_parameters_initialization():
    """Test default and custom initialization of KymogramParameters."""
    params = KymogramParameters(
        parent_name="RawUltrasound",
        line_points=((10.0, 20.0), (30.0, 40.0)),
    )
    assert params.parent_name == "RawUltrasound"
    assert params.line_points == ((10.0, 20.0), (30.0, 40.0))

    meta_dict = params.model_dump()
    assert meta_dict["parent_name"] == "RawUltrasound"
    assert meta_dict["line_points"] == ((10.0, 20.0), (30.0, 40.0))


def test_kymogram_name_generation():
    """Test Kymogram name generation methods."""
    params = KymogramParameters(
        parent_name="RawUltrasound",
        line_points=((0.0, 0.0), (100.0, 100.0)),
    )
    expected_name = "Kymogram on RawUltrasound"
    assert Kymogram.generate_name(params=params) == expected_name

    meta_dict = Kymogram.get_names_and_meta(
        parent="RawUltrasound",
        line_points=((0.0, 0.0), (100.0, 100.0)),
    )
    assert expected_name in meta_dict
    assert meta_dict[expected_name].parent_name == "RawUltrasound"


def test_kymogram_instance_creation(dummy_recording):
    """Test instantiating a Kymogram statistic attached to a Recording."""
    params = KymogramParameters(
        parent_name="RawUltrasound",
        line_points=((5.0, 10.0), (15.0, 20.0)),
    )
    file_info = FileInformation()
    kymogram = Kymogram(
        container=dummy_recording,
        metadata=params,
        file_info=file_info,
    )

    assert kymogram.name == "Kymogram on RawUltrasound"
    assert kymogram.metadata.line_points == ((5.0, 10.0), (15.0, 20.0))

    # Attach to recording statistics dictionary
    dummy_recording.statistics[kymogram.name] = kymogram
    assert "Kymogram on RawUltrasound" in dummy_recording.statistics
    retrieved = dummy_recording.statistics["Kymogram on RawUltrasound"]
    assert retrieved.metadata.line_points == ((5.0, 10.0), (15.0, 20.0))


def test_kymogram_derive_data_raises_not_implemented(dummy_recording):
    """Test that _derive_data raises NotImplementedError prior to Step 4."""
    params = KymogramParameters(
        parent_name="RawUltrasound",
        line_points=((0.0, 0.0), (10.0, 10.0)),
    )
    file_info = FileInformation()
    kymogram = Kymogram(
        container=dummy_recording,
        metadata=params,
        file_info=file_info,
    )
    with pytest.raises(NotImplementedError):
        kymogram._derive_data()
