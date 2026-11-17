import subprocess # To run ping commands.
import platform # To detect OS for ping syntax.
from datetime import datetime # To create timestamps (last_checked)
from storage import load_servers, save_servers


def check_server(server):
    """
    Pings a server to check status, updates its status and last_checked timestamp.
    """
    address = server["address"]

    # Puts status as "down" if address is not found.
    if not address:
        server["status"] = "down"
        server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        return server

    # Check if runnings on Windows, otherwise uses Mac/Linux.
    ping_command = "-n" if platform.system().lower() == "windows" else "-c"
    # Pings the server 1 time.
    command = ["ping", ping_command, "1", address]

    try:
        # Runs the ping command, with 3 sec timeout.
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=3)

        if result.returncode == 0:
            server["status"] = "up"
        else:
            server["status"] = "down"
    # Exception that marks server as down if timedout or unexpected error.
    except (subprocess.TimeoutExpired, Exception):
        server["status"] = "down"

    # Updates the timestamp
    server["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return server


def check_all_servers():
    """
    runs and checks the status of all servers in the list, updating their status and last_checked timestamp.
    """

    servers = load_servers()

    if not servers:
        print("No servers to check in the list.")
        return

    print(f"\n{'Checking server statuses'.center(95)}\n")
    print(f"{'NAME':<15} {'ADDRESS':<15} {'ENVIRONMENT':<15} {'ROLE':<20} {'STATUS':<10} {'LAST CHECKED':<20}")
    print("-" * 95)

    for server in servers:
        name = server["name"]
        address = server["address"]
        environment = server["environment"]
        role = server["role"]

        # Pings server with check_server function from controller.py and updates its new status and last_checked timestamp.
        check_server(server)
        status = server["status"]
        last_checked = server["last_checked"]

        print(
            f"{name:<15} {address:<15} {environment:<15} {role:<20} {status:<10} {last_checked:<20}")

    # saves the updated server list to the data file in storage.py
    save_servers(servers)

    print("\nAll servers have been checked and saved.")
