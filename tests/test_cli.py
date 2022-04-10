from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from trip_extraction import app

runner = CliRunner()


def test_no_filename():

    result = runner.invoke(app, [])

    assert result.exit_code == 2

    assert "Missing argument 'FILENAME'" in result.stdout


@patch("trip_extraction.processor.write_output_file")
def test_cli_running_sample_data(mock_write_output_file):

    result = runner.invoke(
        app, ["data/waypoints.json", "--output", "test.json"]
    )

    assert result.exit_code == 0

    assert result.stdout == ""

    assert mock_write_output_file.call_count == 1


@patch("json.load", MagicMock(return_value=[]))
def test_cli_running_empty_file():

    result = runner.invoke(
        app, ["../data/waypoints.json", "--output", "test.json"]
    )

    assert result.exit_code == 2
