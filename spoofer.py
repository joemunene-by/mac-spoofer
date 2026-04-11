#!/usr/bin/env python3
"""
spoofer.py — MAC Address Spoofer CLI

A Linux-focused tool for viewing, spoofing, and restoring MAC addresses
on network interfaces. Supports random generation, vendor-specific OUI
spoofing, and interface management via `ip link` commands.

Usage:
    sudo python3 spoofer.py --interface eth0 --random
    sudo python3 spoofer.py --interface wlan0 --vendor apple
    sudo python3 spoofer.py --list
    sudo python3 spoofer.py --interface eth0 --show
    sudo python3 spoofer.py --interface eth0 --restore

Requires root privileges for any operation that modifies a MAC address.
"""

import argparse
import os
import random
import re
import subprocess
import sys

try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False

from vendors import VENDORS, get_oui_for_vendor, get_vendor_names, lookup_vendor_by_mac

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------

def _green(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}" if HAS_COLOR else text

def _red(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}" if HAS_COLOR else text

def _yellow(text):
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}" if HAS_COLOR else text

def _cyan(text):
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}" if HAS_COLOR else text

def _bold(text):
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}" if HAS_COLOR else text

# ---------------------------------------------------------------------------
# Stored originals — kept in memory for the lifetime of this process.
# For cross-invocation restore we read from /sys before the first change.
# ---------------------------------------------------------------------------

_original_macs = {}
_ORIGINAL_STORE = "/tmp/.mac_spoofer_originals"


def _save_original(interface, mac):
    """Persist the original MAC so a later invocation can restore it."""
    entries = _load_originals()
    if interface not in entries:
        entries[interface] = mac
        try:
            with open(_ORIGINAL_STORE, "w") as fh:
                for iface, addr in entries.items():
                    fh.write(f"{iface} {addr}\n")
        except OSError:
            pass  # best-effort


def _load_originals():
    """Load previously saved original MACs."""
    entries = {}
    try:
        with open(_ORIGINAL_STORE) as fh:
            for line in fh:
                parts = line.strip().split()
                if len(parts) == 2:
                    entries[parts[0]] = parts[1]
    except FileNotFoundError:
        pass
    return entries

# ---------------------------------------------------------------------------
# MAC validation
# ---------------------------------------------------------------------------

MAC_RE = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")


def validate_mac(mac):
    """Return True if *mac* looks like a valid colon-separated MAC address."""
    return bool(MAC_RE.match(mac))

# ---------------------------------------------------------------------------
# Interface helpers
# ---------------------------------------------------------------------------

def _run(cmd, check=True):
    """Run a shell command and return (stdout, stderr, returncode)."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"Command failed: {' '.join(cmd)}")
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def get_interfaces():
    """Return a dict of {interface_name: mac_address} for all interfaces."""
    interfaces = {}
    try:
        out, _, _ = _run(["ip", "-o", "link", "show"])
        for line in out.splitlines():
            # Example: 2: eth0: <BROADCAST,...> ... link/ether aa:bb:cc:dd:ee:ff ...
            match = re.search(r"^\d+:\s+(\S+?)(?:@\S+)?:", line)
            mac_match = re.search(r"link/ether\s+([0-9a-fA-F:]{17})", line)
            if match:
                name = match.group(1)
                mac = mac_match.group(1) if mac_match else "N/A"
                interfaces[name] = mac
    except Exception as exc:
        print(_red(f"[!] Error listing interfaces: {exc}"))
    return interfaces


def get_mac(interface):
    """Return the current MAC address for *interface*, or None."""
    try:
        path = f"/sys/class/net/{interface}/address"
        with open(path) as fh:
            return fh.read().strip()
    except FileNotFoundError:
        return None


def get_interface_state(interface):
    """Return 'UP' or 'DOWN' (or 'UNKNOWN')."""
    try:
        path = f"/sys/class/net/{interface}/operstate"
        with open(path) as fh:
            return fh.read().strip().upper()
    except Exception:
        return "UNKNOWN"

# ---------------------------------------------------------------------------
# MAC generation
# ---------------------------------------------------------------------------

def generate_random_mac():
    """Generate a fully random unicast, locally-administered MAC address."""
    # First octet: set the locally-administered bit (0x02), clear multicast (0x01).
    first_octet = random.randint(0x00, 0xFF) & 0xFE | 0x02
    octets = [first_octet] + [random.randint(0x00, 0xFF) for _ in range(5)]
    return ":".join(f"{b:02x}" for b in octets)


def generate_vendor_mac(vendor):
    """
    Generate a MAC address using a real OUI from the given vendor.
    The last 3 octets are randomised.
    """
    ouis = get_oui_for_vendor(vendor)
    if ouis is None:
        return None
    oui = random.choice(ouis)
    suffix = ":".join(f"{random.randint(0x00, 0xFF):02x}" for _ in range(3))
    return f"{oui.lower()}:{suffix}"

# ---------------------------------------------------------------------------
# MAC change operations
# ---------------------------------------------------------------------------

def _require_root():
    if os.geteuid() != 0:
        print(_red("[!] This operation requires root privileges. Run with sudo."))
        sys.exit(1)


def set_mac(interface, new_mac):
    """Bring interface down, set the MAC, bring it back up."""
    _require_root()
    current = get_mac(interface)
    if current is None:
        print(_red(f"[!] Interface '{interface}' not found."))
        return False

    # Save original before first change.
    _save_original(interface, current)

    try:
        _run(["ip", "link", "set", "dev", interface, "down"])
        _run(["ip", "link", "set", "dev", interface, "address", new_mac])
        _run(["ip", "link", "set", "dev", interface, "up"])
    except RuntimeError as exc:
        print(_red(f"[!] Failed to set MAC: {exc}"))
        # Try to bring the interface back up regardless.
        subprocess.run(["ip", "link", "set", "dev", interface, "up"],
                       capture_output=True)
        return False

    updated = get_mac(interface)
    if updated and updated.lower() == new_mac.lower():
        print(_green(f"[+] MAC address for {_bold(interface)} changed successfully."))
        print(f"    Old: {_yellow(current)}")
        print(f"    New: {_cyan(updated)}")
        vendor = lookup_vendor_by_mac(updated)
        if vendor:
            print(f"    Vendor: {_bold(vendor)}")
        return True
    else:
        print(_red("[!] MAC address change could not be verified."))
        return False


def restore_mac(interface):
    """Restore the original MAC address for *interface*."""
    _require_root()
    originals = _load_originals()
    original = originals.get(interface)
    if original is None:
        print(_red(f"[!] No saved original MAC for '{interface}'."))
        print("    (Original is only saved when you first change the MAC in this tool.)")
        return False

    current = get_mac(interface)
    if current and current.lower() == original.lower():
        print(_yellow(f"[*] Interface '{interface}' already has its original MAC ({original})."))
        return True

    print(f"[*] Restoring original MAC {_cyan(original)} on {_bold(interface)} ...")
    return set_mac(interface, original)

# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def show_mac(interface):
    """Print the current MAC for a single interface."""
    mac = get_mac(interface)
    if mac is None:
        print(_red(f"[!] Interface '{interface}' not found."))
        return
    state = get_interface_state(interface)
    vendor = lookup_vendor_by_mac(mac) or "Unknown"
    print(f"Interface : {_bold(interface)}")
    print(f"MAC       : {_cyan(mac)}")
    print(f"Vendor    : {vendor}")
    print(f"State     : {'UP' if state == 'UP' else _yellow(state)}")


def list_interfaces():
    """Print a table of all network interfaces and their MACs."""
    ifaces = get_interfaces()
    if not ifaces:
        print(_yellow("[*] No network interfaces found."))
        return

    header = f"{'Interface':<16} {'MAC Address':<20} {'State':<10} {'Vendor'}"
    print(_bold(header))
    print("-" * 65)
    for name, mac in sorted(ifaces.items()):
        state = get_interface_state(name)
        vendor = lookup_vendor_by_mac(mac) or ""
        print(f"{name:<16} {mac:<20} {state:<10} {vendor}")


def list_vendors():
    """Print the available vendor names."""
    names = get_vendor_names()
    print(_bold("Available vendors for OUI spoofing:"))
    for n in names:
        count = len(VENDORS[n])
        print(f"  {n:<14} ({count} OUI{'s' if count != 1 else ''})")

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        description="MAC Address Spoofer -- view, spoof, and restore MAC addresses on Linux.",
        epilog="Examples:\n"
               "  sudo python3 spoofer.py --interface eth0 --random\n"
               "  sudo python3 spoofer.py --interface wlan0 --vendor apple\n"
               "  sudo python3 spoofer.py --interface eth0 --mac AA:BB:CC:DD:EE:FF\n"
               "  sudo python3 spoofer.py --interface eth0 --restore\n"
               "  sudo python3 spoofer.py --list\n"
               "  sudo python3 spoofer.py --vendors\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-i", "--interface",
                        help="Network interface to operate on (e.g. eth0, wlan0)")
    parser.add_argument("-r", "--random", action="store_true",
                        help="Set a random locally-administered MAC address")
    parser.add_argument("-m", "--mac",
                        help="Set a specific MAC address (format: XX:XX:XX:XX:XX:XX)")
    parser.add_argument("-v", "--vendor",
                        help="Spoof MAC using a real OUI from the named vendor (e.g. apple, samsung)")
    parser.add_argument("--restore", action="store_true",
                        help="Restore the original MAC address for the interface")
    parser.add_argument("-l", "--list", action="store_true",
                        help="List all network interfaces with their MAC addresses")
    parser.add_argument("-s", "--show", action="store_true",
                        help="Show the current MAC address for the specified interface")
    parser.add_argument("--vendors", action="store_true",
                        help="List all supported vendor names for OUI spoofing")
    return parser

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = build_parser()
    args = parser.parse_args()

    # --- Actions that do NOT require an interface ---
    if args.list:
        list_interfaces()
        return

    if args.vendors:
        list_vendors()
        return

    # --- All remaining actions require --interface ---
    if not args.interface:
        parser.print_help()
        print(_yellow("\n[*] Provide --interface or use --list / --vendors."))
        sys.exit(1)

    interface = args.interface

    # Verify interface exists.
    if get_mac(interface) is None:
        print(_red(f"[!] Interface '{interface}' does not exist."))
        sys.exit(1)

    if args.show:
        show_mac(interface)
        return

    if args.restore:
        restore_mac(interface)
        return

    if args.mac:
        if not validate_mac(args.mac):
            print(_red(f"[!] Invalid MAC address format: '{args.mac}'"))
            print("    Expected format: XX:XX:XX:XX:XX:XX")
            sys.exit(1)
        set_mac(interface, args.mac)
        return

    if args.vendor:
        vendor = args.vendor.lower()
        if vendor not in VENDORS:
            print(_red(f"[!] Unknown vendor '{args.vendor}'."))
            list_vendors()
            sys.exit(1)
        new_mac = generate_vendor_mac(vendor)
        print(f"[*] Generating {_bold(args.vendor.capitalize())} MAC address ...")
        set_mac(interface, new_mac)
        return

    if args.random:
        new_mac = generate_random_mac()
        print("[*] Generating random MAC address ...")
        set_mac(interface, new_mac)
        return

    # No action selected — show current MAC as default.
    show_mac(interface)


if __name__ == "__main__":
    main()
