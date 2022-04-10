import json
from pathlib import Path
from typing import Any, Dict, List

from trip_extraction.exceptions import EmptyFile
from trip_extraction.logger import logger
from trip_extraction.model import Car, Waypoint


def read_data_file(filename: Path) -> List[Dict[str, Any]]:

    with open(filename) as json_file:
        data = json.load(json_file)

    if not data or not isinstance(data, list):
        raise EmptyFile()

    return data


def write_output_file(output: Path, results: List[Dict[str, Any]]) -> None:

    with open(output, "w") as outfile:
        json.dump(results, outfile, indent=2)


def process_file_inputs(
    filename: Path, output: Path = Path("trips.json")
) -> None:
    """
    process a given filename

    :param filename: filename to process
    :param output: filename to save all trip results
    :return:
    """

    try:
        records = read_data_file(filename)
    except Exception as er:
        logger.error(f"Error found reading the file: {filename} {er}")
        exit(2)

    car = Car()
    for record in records:
        wp = Waypoint(**record)

        car.record_point(wp)

    if not car.trips:
        logger.warning("No trips found to Export.")
        return

    try:
        write_output_file(output, [trip.to_dict() for trip in car.trips])
    except Exception as er:
        logger.error(f"Error {er} saving output file.")

    logger.info("File processed successfully")
