import argparse
import os
import sys
import time
from typing import NoReturn
from rich.table import Table
from core.interface import list_interfaces_with_details, get_interface_details
from core.spoofer import change_mac, restore_mac, generate_random_mac, run_interval_mode, SpooferError
from core.validator import MACValidationError
from core.vendor import generate_vendor_mac, list_vendors
from core.profiles import save_profile, get_profile_mac, list_profiles
from cli.tui import tui_menu, display_interfaces_detailed
from utils.logger import setup_logger, console, print_success, print_error, print_warning, print_info

logger = setup_logger("mac_spoofer")

DISCLAIMER_PATH = os.path.expanduser("~/.mac_spoofer_disclaimer_accepted")

def check_disclaimer() -> None:
    """Ensures the user has accepted the disclaimer."""
    if os.path.exists(DISCLAIMER_PATH):
        return

    console.print("\n[bold]DISCLAIMER[/bold]")
    console.print("This tool is for authorized educational and ethical testing only.")
    console.print("The author is not responsible for any misuse or damage caused.")
    console.print("By using this tool, you agree to these terms.")
    
    response = input("\nAccept terms? (y/n): ").strip().lower()
    if response == 'y':
        with open(DISCLAIMER_PATH, 'w') as f:
            f.write("accepted")
        print_success("Disclaimer accepted.")
    else:
        print_error("Disclaimer rejected. Exiting.")
        sys.exit(0)

def display_interfaces() -> None:
    """Lists all available interfaces in a clean, simple table."""
    interfaces = list_interfaces_with_details()
    table = Table(show_header=True, header_style="bold", box=None)
    table.add_column("Interface")
    table.add_column("MAC Address")

    for iface in interfaces:
        table.add_row(iface["interface"], iface["mac"])
    
    console.print(table)

def clear_history() -> None:
    """Clears shell history for stealth."""
    try:
        shell = os.environ.get("SHELL", "")
        if "bash" in shell:
            os.system("history -c")
        elif "zsh" in shell:
            os.system("fc -p")
    except Exception:
        pass

def main() -> None:
    check_disclaimer()

    parser = argparse.ArgumentParser(
        description="Professional MAC Address Spoofer for Linux",
        epilog="Example: sudo mac-spoofer -i eth0 -r"
    )
    parser.add_argument("-i", "--interface", help="Network interface to spoof")
    parser.add_argument("-m", "--mac", help="Specific MAC address to set")
    parser.add_argument("-r", "--random", action="store_true", help="Generate a random MAC address")
    parser.add_argument("-v", "--vendor", help="Spoof as vendor (e.g. 'Samsung', 'Apple' or 'random')")
    parser.add_argument("--interval", type=int, help="Rotate MAC every N minutes")
    parser.add_argument("--save-profile", help="Save current MAC to named profile")
    parser.add_argument("--load-profile", help="Load MAC from named profile")
    parser.add_argument("--list-profiles", action="store_true", help="List saved profiles")
    parser.add_argument("--restore", action="store_true", help="Restore the original MAC address")
    parser.add_argument("-l", "--list", action="store_true", help="List all interfaces and details")
    parser.add_argument("--stealth", action="store_true", help="Clear terminal history after execution")
    parser.add_argument("--silent", action="store_true", help="Suppress all output")

    args = parser.parse_args()

    if args.silent:
        sys.stdout = open(os.devnull, 'w')

    # Check for root privileges if modifying MAC
    if (args.mac or args.random or args.restore or args.vendor or args.interval or args.load_profile) and os.getuid() != 0:
        print_error("This operation requires root privileges (sudo).")
        sys.exit(1)

    try:
        if args.list:
            display_interfaces_detailed(list_interfaces_with_details())
        elif args.list_profiles:
            profiles = list_profiles()
            print_info(f"Profiles: {', '.join(profiles)}")
        elif args.interface:
            if args.save_profile:
                details = get_interface_details(args.interface)
                if save_profile(args.save_profile, details["mac"]):
                    print_success(f"Profile '{args.save_profile}' saved: {details['mac']}")
            elif args.load_profile:
                mac = get_profile_mac(args.load_profile)
                if mac and change_mac(args.interface, mac):
                    print_success(f"Profile '{args.load_profile}' applied to {args.interface}")
            elif args.restore:
                if restore_mac(args.interface):
                    print_success(f"MAC address restored for {args.interface}")
            elif args.interval:
                run_interval_mode(args.interface, args.interval, args.vendor or "random")
            elif args.vendor:
                new_mac = generate_vendor_mac(args.vendor)
                if change_mac(args.interface, new_mac):
                    print_success(f"MAC for {args.interface} changed to {new_mac} ({args.vendor})")
            elif args.random:
                new_mac = generate_random_mac()
                if change_mac(args.interface, new_mac):
                    print_success(f"MAC for {args.interface} changed to {new_mac}")
            elif args.mac:
                if change_mac(args.interface, args.mac):
                    print_success(f"MAC for {args.interface} changed to {args.mac}")
            else:
                details = get_interface_details(args.interface)
                print_info(f"Interface: {args.interface} | MAC: {details['mac']} | Vendor: {details['vendor']}")
        elif not any(vars(args).values()):
            tui_menu()
            
        if args.stealth:
            clear_history()

    except (SpooferError, MACValidationError) as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.exception("An unexpected error occurred")
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
