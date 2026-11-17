
# Server Inventory Tool

## 1. About the Project

Server Inventory Tool is a Python program that helps users manage and monitor servers.

With this program, users can view server information from a JSON file, add servers, remove servers, check if servers are online and export server information to CSV files.

All server information is saved in a JSON file.

Servers are organized into three environments:

- `dev` - Development servers.
- `test` - Test servers.
- `prod` - Production servers.

## 2. Features

The program includes:

- Display all servers.
- Filter servers by environment.
- Add new servers.
- Remove existing servers.
- Check the status of one server.
- Check the status of all servers.
- Save the latest server check time.
- Export server information to CSV.
- Choose where server information is saved using an environment variable.

When removing a production server, the program asks for confirmation.

## 3. Requirements

To run the program, you need:

- Python 3 installed.
- A terminal or command prompt.
- A working `ping` command.

The program only uses built-in Python modules. No additional packages need to be installed.

The program supports two ways of running it:

- **Interactive Mode:** A menu where users select different options by entering a number.
- **CLI Mode:** Run different commands directly in the terminal.

## 4. Project Structure

The project contains the following files and folders:

```text
Server-Inventory-Tool/
│
├── main.py
├── menu.py
├── controller.py
├── storage.py
├── servers.json
│
└── reports/
```

File descriptions:

- `main.py` - Starts the program and handles CLI commands.
- `menu.py` - Contains the interactive menu and its functions.
- `controller.py` - Checks if servers are online or offline.
- `storage.py` - Handles JSON storage and CSV exports.
- `servers.json` - Stores server information.
- `reports/` - Stores exported CSV reports.

## 5. How to Run the Program

### Interactive Mode

To start the program with the interactive menu, run:

```bash
python3 main.py
```

The menu allows users to select different options by entering a number.

### CLI Mode

The program can also be controlled directly from the terminal using command-line arguments.

Available commands:

| Command | What it does |
|---|---|
| `python3 main.py --list` | Displays all servers. |
| `python3 main.py --list --env dev` | Displays development servers. |
| `python3 main.py --list --env test` | Displays test servers. |
| `python3 main.py --list --env prod` | Displays production servers. |
| `python3 main.py --check SERVERNAME` | Checks a specific server. |
| `python3 main.py --check-all` | Checks all servers. |
| `python3 main.py --export` | Exports a CSV report. |

To see all available commands, run:

```bash
python3 main.py --help
```
The help command displays all available commands and explains how to use them.

The program returns an exit code:

- `0` means the operation was successful and all checked servers are online.
- `1` means a server is down or an error occurred.

## 6. Environment Variable

The program uses an environment variable called `INVENTORY_DATAFIL`.

This variable decides where the server information is loaded from and saved to.

By default, the program uses a file called:

`servers.json`

If you want to use another JSON file, set the environment variable before starting the program.

### Windows (PowerShell)

```powershell
$env:INVENTORY_DATAFIL = "C:\ServerData\servers.json"
python3 main.py
```

### Windows (Command Prompt)

```cmd
set INVENTORY_DATAFIL=C:\ServerData\servers.json
python main.py
```

### Linux / macOS

```bash
export INVENTORY_DATAFIL=/home/user/serverdata/servers.json
python3 main.py
```
The path can be absolute or relative to the current working directory.

For example, if the environment variable is set to:

`./data/my_servers.json`

The program will use that file instead of the default `servers.json`.

The directory containing the custom JSON file must already exist.

If no environment variable is set, the program automatically uses `servers.json`.

## 7. Server Data

Each server has the following information:

| Field | Description |
|---|---|
| `name` | The name of the server. |
| `address` | The server's IP address or hostname. |
| `environment` | dev, test or prod. |
| `role` | What the server is used for. |
| `status` | Current status: up, down or unknown. |
| `last_checked` | Date and time of the latest check. |

Example of a server in the JSON file:

```json
{
  "name": "web01",
  "address": "example.com",
  "environment": "prod",
  "role": "web-server",
  "status": "up",
  "last_checked": "2026-11-17 17:47"
}
```

If the JSON file does not exist, the program starts with an empty server list.

## 8. Server Checks and CSV Reports

The program checks servers using the `ping` command.

It automatically detects the operating system and uses the correct command:

- Windows: `ping -n 1`
- Linux/macOS: `ping -c 1`

Each server is pinged once, with a timeout of three seconds.

If the server responds, its status is set to `up`. Otherwise, the status is set to `down`.

The program also saves the date and time of the latest check.

**Note:** A server can be online even if it does not respond to ping. Firewalls and network settings can block ping requests.

### CSV Export

The program can export server information to a CSV file.

Reports are automatically saved in the `reports/` folder.

Each report gets a filename containing the date and time, for example:

```text
reports/inventory_2026-11-17_1747.csv
```

The CSV file contains the server name, address, environment, role, status and latest check time.