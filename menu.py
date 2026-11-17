import sys # Handles exitcodes.
from controller import check_all_servers, check_server
from storage import load_servers, save_servers, export_to_csv


def show_menu():
    """
    Runs the main menu loop.
    """

    while True:
        print("\n=== Server Inventory Tool ===\n")
        print("======== MENU =========")
        print("1. Display all servers")
        print("2. Display servers in a specific environment")
        print("3. Add a new server")
        print("4. Remove a server")
        print("5. Check a specific server")
        print("6. Check all servers")
        print("7. Export report of servers as CSV")
        print("8. Exit")

        # Accepts the user input and removes spaces.
        choice = input("\nChoose an option (1-8): ").strip()

        # Controlls the functions with different choices (1-8)
        if choice == "1":
            display_all_servers()

        elif choice == "2":
            display_servers_by_environment()

        elif choice == "3":
            add_server()

        elif choice == "4":
            remove_server()

        elif choice == "5":
            run_check_server()

        elif choice == "6":
            check_all_servers()

        elif choice == "7":
            export_server_report()

        elif choice == "8":
            print("Exiting the program.")
            sys.exit(0)

        else:
            print("Invalid choice. Please enter a valid option (1-8).")


def display_all_servers():
    """
    Displays all the servers in the list.
    """

    # Loads all the servers.
    servers = load_servers()

    # Checks if the list is empty.
    if not servers:
        print("\nNo servers to display.")
        return

    # Prints the header
    print(f"\n{'All Servers'.center(95)}\n")
    print(f"{'NAME':<15} {'ADDRESS':<15} {'ENVIRONMENT':<15} {'ROLE':<20} {'STATUS':<10} {'LAST CHECKED':<20}")
    print("-" * 95)

    # Loops all the servers in the list and prints the servers.
    for server in servers:
        name = server["name"]
        address = server["address"]
        environment = server["environment"]
        role = server["role"]
        status = server["status"]
        last_checked = server["last_checked"]

        print(
            f"{name:<15} {address:<15} {environment:<15} {role:<20} {status:<10} {last_checked:<20}")
    print("-" * 95)


def display_servers_by_environment():
    """
    Displays servers filtered by a specific environment.
    """

    servers = load_servers()

    if not servers:
        print("\nNo servers to display.")
        return

    # Sets valid environments
    valid_environments = ["dev", "test", "prod"]
    
    # Loops until the users environment choice is valid.
    while True:
        environment = input(
            "\nEnter the environment (dev/test/prod): ").strip().lower()
        if environment in valid_environments:
            break
        print("Invalid environment. Please enter dev, test, or prod.")

    # Filters out the matching server in the environment.
    filtered_servers = [
        server for server in servers if server["environment"].strip().lower() == environment]

    if not filtered_servers:
        print(f"\nNo servers found in '{environment}' environment.")
        return

    print(f"\n{f'Servers in [{environment}] environment'.center(95)}\n")
    print(f"{'NAME':<15} {'ADDRESS':<15} {'ENVIRONMENT':<15} {'ROLE':<20} {'STATUS':<10} {'LAST CHECKED':<20}")
    print("-" * 95)

    for server in filtered_servers:
        name = server["name"]
        address = server["address"]
        environment = server["environment"]
        role = server["role"]
        status = server["status"]
        last_checked = server["last_checked"]

        print(
            f"{name:<15} {address:<15} {environment:<15} {role:<20} {status:<10} {last_checked:<20}")
    print("-" * 95)


def add_server():
    """
    Adds a new server to the list.
    """

    servers = load_servers()

    # Validates the servername. A quit option is added to make it user-friendly.
    while True:
        name = input("Enter server name (or QUIT to cancel): ").strip()
        if name.upper() == "QUIT":
            print("Server addition cancelled.")
            return

        # Stops the user from adding an empty servername.
        if not name:
            print("\nServer name cannot be empty. Please enter a valid name.")
            continue

        # Stops the user from adding a servername that already exists.
        if any(server["name"].lower() == name.lower() for server in servers):
            print(
                f"\nA server with the name '{name}' already exists. Please choose a different name.")
            continue
        break

    # Validates the server-address. 
    while True:
        address = input("Enter server address (or QUIT to cancel): ").strip()
        if address.upper() == "QUIT":
            print("Server addition cancelled.")
            return

        if not address:
            print("\nServer address cannot be empty. Please enter a valid address.")
            continue
        break

    valid_environments = ["dev", "test", "prod"]
    while True:
        environment = input(
            "Enter server environment (dev/test/prod or QUIT to cancel): ").strip().lower()
        if environment.upper() == "QUIT":
            print("Server environment addition cancelled.")
            return
        if environment in valid_environments:
            break
        print("Invalid environment. Please enter dev, test, or prod.")

    while True:
        role = input("Enter server role (or QUIT to cancel): ").strip()
        if role.upper() == "QUIT":
            print("Server role addition cancelled.")
            return

        if not role:
            print("Server role cannot be empty. Please enter a valid role.")
            continue
        break

    # Creater the new server with status: "unknown".
    new_server = {
        "name": name,
        "address": address,
        "environment": environment,
        "role": role,
        "status": "unknown",
        "last_checked": ""
    }

    # Adds the new server to the list and saves it in the file.
    servers.append(new_server)
    save_servers(servers)
    print(f"\nServer '{name}' has been added successfully.")


def remove_server():
    """
    Removes a server from the list
    """

    servers = load_servers()

    if not servers:
        print("\nNo servers to remove.")
        return

    while True:
        name = input(
            "Enter the name of the server to remove (or QUIT to cancel): ").strip()
        if name.upper() == "QUIT":
            print("Server removal cancelled.")
            return

        if not name:
            print("Server name cannot be empty. Please enter a valid name.")
            continue

        found_server = None
        for server in servers:
            if server["name"].lower() == name.lower():
                found_server = server
                break

        if not found_server:
            print(f"\nNo server found with name: '{name}'.")
            continue
        break

    # Requires extra confirmation when trying to remove a "prod" server.
    if found_server["environment"].strip().lower() == "prod":

        while True:
            confirmation = input(
                f"\nAre you sure you want to remove the production server '{name}'? (yes/no): ").strip().lower()

            if confirmation == "yes":
                break
            elif confirmation == "no":
                print("Server removal cancelled.")
                return
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    # Removes the server from the list and saves it.
    servers.remove(found_server)
    save_servers(servers)
    print(f"\nServer '{name}' has been removed successfully.")


def run_check_server():
    """
    runs the check_server function from controller.py to check the status of a specific server in the list.
    """

    servers = load_servers()

    if not servers:
        print("\nNo servers to check.")
        return

    while True:
        name = input(
            "Enter the name of the server (or QUIT to cancel): ").strip()
        if name.upper() == "QUIT":
            print("Server check cancelled.")
            return

        if not name:
            print("\nServer name cannot be empty. Please enter a valid name.")
            continue

        found_server = None
        for server in servers:
            if server["name"].lower() == name.lower():
                found_server = server
                break

        if not found_server:
            print(f"\nNo server found with name: '{name}'.")
            continue
        break

    print(f"\nChecking [{found_server['name']}] server status\n")

    # Pings server with check_server function from controller.py and updates its status and last_checked timestamp.
    check_server(found_server)

    # saves the updated server list to the data file in storage.py
    save_servers(servers)

    print(f"{'NAME':<15} {'ADDRESS':<15} {'ENVIRONMENT':<15} {'ROLE':<20} {'STATUS':<10} {'LAST CHECKED':<20}")
    print("-" * 95)
    print(f"{found_server['name']:<15} {found_server['address']:<15} {found_server['environment']:<15} {found_server['role']:<20} {found_server['status']:<10} {found_server['last_checked']:<20}")

def export_server_report():
    """
    Loads servers and exports them to a CSV file if there's servers in the list.
    """
    servers = load_servers()

    # No CSV-file is created if there's no servers in the list.
    if not servers:
        print("\nNo servers to export.")
        return

    # Calls the function from storage.py
    export_to_csv(servers)
