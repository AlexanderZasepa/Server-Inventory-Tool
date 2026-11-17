import storage
from menu import show_menu # Runs the main menu.
from controller import check_server # Pings and updates timestamps.
import argparse  # Handles argparse commands.
import sys  # Handles exitcodes.


def main():
    """
    Starts the Server Inventory Tool. (Interactive text menu and CLI args)
    """

    # Creates argumentparser for the command-flags in the terminal.
    parser = argparse.ArgumentParser(
        description="Server Inventory Tool - Manage and check your servers."
    )

    # All the command-flags.
    parser.add_argument("--list", action="store_true",
                        help="Prints all servers and exit")
    parser.add_argument("--env", type=str,
                        help="Filters servers by environment. --list --env (dev, test, prod)")
    parser.add_argument("--check", type=str, metavar="NAME",
                        help="Checks a specific server by name")
    parser.add_argument("--check-all", action="store_true",
                        help="Checks all servers")
    parser.add_argument("--export", action="store_true",
                        help="Exports report of servers to CSV")

    # Read the users argument and loads the servers.
    args = parser.parse_args()
    servers = storage.load_servers()

    # Handles --list and filter with --env.
    if args.list:
        env_filter = args.env.lower() if args.env else None
        print(f"{'NAME':<15} {'ADDRESS':<15} {'ENVIRONMENT':<15} {'ROLE':<20} {'STATUS':<10} {'LAST CHECKED':<20}")
        print("-" * 95)

        found = False
        for server in servers:
            try:
                env = server["environment"]
                if env_filter and env != env_filter:
                    continue
                found = True
                print(
                    f"{server['name']:<15} {server['address']:<15} {env:<15} {server['role']:<20} {server['status']:<10} {server['last_checked']:<20}")
            except KeyError as err:
                print(f"Error: Missing server data field: {err}")
                sys.exit(1)

        if env_filter and not found:
            print(f"No servers found in the environment '{env_filter}'")

        sys.exit(0)

    # Handles --check for a specific server in the list.
    elif args.check:
        target_name = args.check
        server_found = False
        server_is_down = False

        for server in servers:
            try:
                if server["name"].lower() == target_name.lower():
                    server_found = True
                    print(f"Checking server [{server['name']}]")

                    # Function from controller.py that pings and updates last_checked timestamp.
                    check_server(server)

                    if server["status"] == "down":
                        server_is_down = True
                    break
            except KeyError as err:
                print(f"Error: Missing server data field: {err}")
                sys.exit(1)
        if not server_found:
            print(f"Error: Server '{target_name}' was not found")
            sys.exit(1)

        storage.save_servers(servers)
        print(f"Server [{server['name']}] has been checked.")


        if server_is_down:
            sys.exit(1)
        else:
            sys.exit(0)

    # Handles --check-all for all servers in the list.
    elif args.check_all:
        print("Checking all servers")
        any_server_down = False

        for server in servers:
            try:
                # Function from controller.py that pings and updates last_checked timestamps.
                check_server(server)
                
                if server["status"] == "down":
                    any_server_down = True
            except KeyError as err:
                print(f"Error: Missing server data field: {err}")
                sys.exit(1)

        storage.save_servers(servers)
        print("All servers checked and saved")

        if any_server_down:
            sys.exit(1)
        else:
            sys.exit(0)

    # Handles --export to export a CSV-report. 
    elif args.export:
        filename = storage.export_to_csv(servers)
        sys.exit(0)

    # Starts the interactive menu if no flags are given.
    else:

        show_menu()

# Main() runs only when the file is executed directly.
if __name__ == "__main__":
    main()
