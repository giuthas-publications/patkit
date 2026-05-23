"""
Integration tests for the PATKIT CLI.

These tests automate the CLI invocations previously found in
`integration_tests.sh`. The GUI and interactive interpreters
are mocked out to prevent the automated test suite from hanging.
"""
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from patkit.cli import run_cli


@pytest.fixture
def runner() -> CliRunner:
    """
    Provide a Click CLI runner for testing commands.

    Returns
    -------
    CliRunner
        The test runner.
    """
    return CliRunner()


def test_cli_bare(runner: CliRunner) -> None:
    """
    Test running patkit with no arguments.

    Parameters
    ----------
    runner : CliRunner
        The Click CLI runner.
    """
    result = runner.invoke(run_cli, catch_exceptions=False)
    # Depending on how your root command is configured, it may exit 0
    # and print help, or exit 2 due to missing arguments.
    assert result.exit_code in (0, 2)


def test_cli_help(runner: CliRunner) -> None:
    """
    Test running patkit with the --help flag.

    Parameters
    ----------
    runner : CliRunner
        The Click CLI runner.
    """
    result = runner.invoke(run_cli, args=["--help"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "Usage:" in result.output


@patch("patkit.cli_commands.run_annotator")
def test_cli_default_minimal(
    mock_annotator: MagicMock, runner: CliRunner
) -> None:
    """
    Test running patkit against the minimal scenario implicitly.

    Parameters
    ----------
    mock_annotator : MagicMock
        Mock to prevent GUI blocking.
    runner : CliRunner
        The Click CLI runner.
    """
    result = runner.invoke(
        run_cli, args=["scenarios/minimal"], catch_exceptions=False
    )
    assert result.exit_code == 0
    mock_annotator.assert_called_once()


@patch("patkit.cli_commands.run_annotator")
def test_cli_open_minimal(
    mock_annotator: MagicMock, runner: CliRunner
) -> None:
    """
    Test running the patkit open command on the minimal scenario.

    Parameters
    ----------
    mock_annotator : MagicMock
        Mock to prevent GUI blocking.
    runner : CliRunner
        The Click CLI runner.
    """
    result = runner.invoke(
        run_cli, args=["open", "scenarios/minimal/"], catch_exceptions=False
    )
    assert result.exit_code == 0
    mock_annotator.assert_called_once()


@patch("patkit.cli_commands.run_annotator")
def test_cli_default_tongue_data(
    mock_annotator: MagicMock, runner: CliRunner
) -> None:
    """
    Test running patkit against tongue_data_1_1 implicitly.

    Parameters
    ----------
    mock_annotator : MagicMock
        Mock to prevent GUI blocking.
    runner : CliRunner
        The Click CLI runner.
    """
    result = runner.invoke(
        run_cli,
        args=["scenarios/tongue_data_1_1/"],
        catch_exceptions=False
    )
    assert result.exit_code == 0
    mock_annotator.assert_called_once()


@patch("patkit.cli_commands.run_interpreter")
def test_cli_interact_minimal(
    mock_interpreter: MagicMock, runner: CliRunner
) -> None:
    """
    Test running the interact command on the minimal scenario.

    Parameters
    ----------
    mock_interpreter : MagicMock
        Mock to prevent REPL blocking.
    runner : CliRunner
        The Click CLI runner.
    """
    result = runner.invoke(
        run_cli,
        args=["interact", "scenarios/minimal/"],
        catch_exceptions=False
    )
    assert result.exit_code == 0
    mock_interpreter.assert_called_once()
