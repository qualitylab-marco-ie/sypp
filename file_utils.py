import json, csv
import logging
import debug_utils as debug_utils
from datetime import datetime

from pathlib import Path

# csv_file = "data.csv"
#csv_file = f"{datetime.now().strftime('%Y-%m-%d')}.csv"
json_file = "data.json"
path = Path(f"data").resolve()


def run_file_checks() -> bool:    
    debug_utils.debug_message("Running file checks...", logging.INFO)

    script_dir = Path(__file__).resolve().parent  # This will give the directory inside src
    file_path = script_dir / "data" / f"{datetime.now().strftime('%Y-%m-%d')}.csv"

    if not _check_file(file_path):
        return _create_file(file_path)

    return True


def _check_file(file_path: Path) -> bool:
    if file_path.exists():
        debug_utils.debug_message(f"File '{file_path}' already exists.", logging.INFO)
        return True

    debug_utils.debug_message(f"File '{file_path}' does not exist.", logging.INFO)
    return False


def _create_file(file_path: Path) -> bool:
    try:
        with open(file_path, mode="w", newline="") as file:
            debug_utils.debug_message("Creating file...", logging.INFO)

            csv_header = [
                "pump",
                "start_time",
                "end_time",
                "elapsed_time_ms",
                "flow_rate",
                "volume",
                "total_volume",
                "pulse_count"
            ]
            writer = csv.writer(file)
            writer.writerow(csv_header)  # Write the header

            debug_utils.debug_message("Done!", logging.INFO)
            return True
    except Exception as e:
        debug_utils.debug_message(f"Error creating file: {e}", logging.INFO)
        return False


def csv_to_json(file_path: Path) -> bool:
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)

        json_file_path = path / json_file
        with open(json_file_path, mode="w", encoding="utf-8") as file:
            json.dump(rows, file, indent=4)

        debug_utils.debug_message(f"CSV data successfully converted to JSON at {json_file_path}.", logging.INFO)
        return True
    except FileNotFoundError:
        debug_utils.debug_message(f"Error: The file '{file_path}' was not found.", logging.INFO)
    except json.JSONDecodeError as e:
        debug_utils.debug_message(f"Error: Failed to decode JSON data. {e}", logging.INFO)
    except csv.Error as e:
        debug_utils.debug_message(f"Error: Failed to read CSV file. {e}", logging.INFO)
    except Exception as e:
        debug_utils.debug_message(f"Unexpected error: {e}", logging.INFO)

    return False


def append_to_file(data: dir) -> None:
    #file_path = path / f"{datetime.now().strftime('%Y-%m-%d')}.csv"

    script_dir = Path(__file__).resolve().parent  # This will give the directory inside src
    file_path = script_dir / "data" / f"{datetime.now().strftime('%Y-%m-%d')}.csv"

    run_file_checks()

    csv_header = [
        "pump",
        "start",
        "end",
        "elapsed_ms",
        "flow_rate",
        "volume",
        "total_volume",
        "pulses"
    ]

    try:
        with open(file_path, mode="a", newline="") as file:
            debug_utils.debug_message(f"Appending data to {file_path}...", logging.INFO)

            writer = csv.DictWriter(file, fieldnames=csv_header)

            # Only write header if file is empty
            file_empty = file.tell() == 0
            if file_empty:
                writer.writeheader()

            writer.writerow(data)

            #writer = csv.writer(file)
            #writer.writerow(data)

            debug_utils.debug_message("Data appended successfully.", logging.INFO)
    except (OSError, IOError) as e:
        debug_utils.debug_message(f"File operation error: {e}", logging.INFO)
    except Exception as e:
        debug_utils.debug_message(e, logging.INFO)
