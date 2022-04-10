__version__ = "0.1.0"
from pathlib import Path

import typer

from trip_extraction.processor import process_file_inputs

app = typer.Typer()


@app.command()
def main(
    filename: Path,
    output: Path = typer.Option(
        "trips.json", help="Filename for the result output."
    ),
) -> None:
    """This program process a filename with Waypoints and save all resulting trips into an output."""
    process_file_inputs(filename, output)
