import os # Reads the environment variable that determines the path to the JSON file.
import json # To read and write data in JSON format.
import csv # To create and write CSV report
from pathlib import Path # To handle safe and modern file path.
from datetime import datetime # To generate timestamps 

# functions for JSON-storage and CSV-export of servers.


def get_data_path():
    """
    Reads the data file path from the environment variable INVENTORY_DATAFIL.
    If the environment variable is not set, defaults to "servers.json".
    """
    filename = os.getenv("INVENTORY_DATAFIL", "servers.json")
    return Path(filename)


def load_servers():
    """
    Loads servers from the JSON file.
    If the data file does not exist, the program starts with an empty list instead of crashing.
    """
    path = get_data_path()
    if not path.exists():
        return []

    try:
        # Opens the JSON file in read mode.
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Returns empty list if the JSON file is empty or broken.
        return []


def save_servers(servers):
    """
    Saves the list of servers.
    """
    path = get_data_path()
    # Opens the JSON file in write mode and dumps the server list as JSON.
    with open(path, "w", encoding="utf-8") as file:
        json.dump(servers, file, indent=2, ensure_ascii=False)


def export_to_csv(servers):
    """
    Exports the list of servers to a CSV file in the reports directory including date and time.
    """
    reports_dir = Path("reports")

    try:
        # Creates the reports directory.
        reports_dir.mkdir(exist_ok=True)

        # Creates a new filename with timestamps.
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        filename = reports_dir / f"inventory_{timestamp}.csv"

        # Opens the CSV file in writer mode.
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # Writes the header.
            writer.writerow(["name", "address", "environment",
                             "role", "status", "last_checked"])

            # Loops the server list and writes the details to CSV.
            for server in servers:

                name = server["name"]
                address = server["address"]
                environment = server["environment"]
                role = server["role"]
                status = server["status"]
                last_checked = server["last_checked"]

                writer.writerow([name, address, environment,
                                 role, status, last_checked])

        print(f"\nReport of servers exported successfully. [{filename}]")
        return filename

    # Throw exception if there's no permission to write files.
    except PermissionError:
        print("Permission denied: Unable to create reports to directory.")
        return None
    # Throws exception if the directory is not found.
    except FileNotFoundError:
        print("File not found: Unable to create reports to directory.")
        return None
