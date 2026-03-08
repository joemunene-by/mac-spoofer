import os
import sys
import time
from typing import List
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from core.interface import list_interfaces_with_details
from core.spoofer import change_mac, generate_random_mac, restore_mac
from core.vendor import generate_vendor_mac, list_vendors
from core.profiles import list_profiles, get_profile_mac
from utils.logger import console, print_success, print_error, print_info

def create_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    return layout

def get_interface_table() -> Table:
    table = Table(show_header=True, header_style="bold", box=None, expand=True)
    table.add_column("Interface")
    table.add_column("Type")
    table.add_column("State")
    table.add_column("IP")
    table.add_column("MAC")
    table.add_column("Vendor")

    for details in list_interfaces_with_details():
        state_color = "green" if details["state"] == "UP" else "red"
        table.add_row(
            details["interface"],
            details["type"],
            f"[{state_color}]{details['state']}[/{state_color}]",
            details["ip"],
            details["mac"],
            details["vendor"]
        )
    return table

def run_tui() -> None:
    """Runs a simple interactive TUI."""
    layout = create_layout()
    layout["header"].update(Panel("MAC Address Spoofer - Interactive Mode", style="bold blue"))
    layout["footer"].update(Panel("Press 'q' to quit | 'r' to refresh | 's' to spoof", style="dim"))

    with Live(layout, refresh_per_second=1, screen=True):
        while True:
            layout["body"].update(get_interface_table())
            # Simple input handling in TUI is limited without full textual,
            # so we use this for live monitoring mostly.
            # Real interactive input would happen here.
            time.sleep(1)
            # In a real implementation, we'd use a non-blocking key listener.
            break # Exit for now as we don't have a full key listener implemented

def tui_menu() -> None:
    """A CLI-based interactive menu."""
    while True:
        console.clear()
        console.print("[bold blue]MAC Address Spoofer - Menu[/bold blue]\n")
        
        interfaces = list_interfaces_with_details()
        display_interfaces_detailed(interfaces)
        
        console.print("\n1. Spoof Interface (Random)")
        console.print("2. Spoof Interface (Vendor)")
        console.print("3. Restore Original MAC")
        console.print("4. Load Profile")
        console.print("5. Quit")
        
        choice = input("\nSelect an option: ").strip()
        
        if choice == '5':
            break
        
        if choice in ['1', '2', '3', '4']:
            idx = input("Enter interface name: ").strip()
            if choice == '1':
                new_mac = generate_random_mac()
                change_mac(idx, new_mac)
            elif choice == '2':
                vendors = list_vendors()
                print(f"Available vendors: {', '.join(vendors)}")
                v = input("Vendor name: ").strip()
                new_mac = generate_vendor_mac(v)
                change_mac(idx, new_mac)
            elif choice == '3':
                restore_mac(idx)
            elif choice == '4':
                profiles = list_profiles()
                print(f"Available profiles: {', '.join(profiles)}")
                p = input("Profile name: ").strip()
                mac = get_profile_mac(p)
                if mac:
                    change_mac(idx, mac)
            input("\nPress Enter to continue...")

def display_interfaces_detailed(interfaces: List[dict]) -> None:
    table = Table(show_header=True, header_style="bold", box=None)
    table.add_column("Interface")
    table.add_column("Type")
    table.add_column("State")
    table.add_column("IP")
    table.add_column("MAC")
    table.add_column("Vendor")

    for details in interfaces:
        state_color = "green" if details["state"] == "UP" else "red"
        table.add_row(
            details["interface"],
            details["type"],
            f"[{state_color}]{details['state']}[/{state_color}]",
            details["ip"],
            details["mac"],
            details["vendor"]
        )
    console.print(table)
