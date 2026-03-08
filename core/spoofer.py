import random
import subprocess
import os
import json
import time
from typing import Optional
from core.validator import normalize_mac, MACValidationError
from core.interface import get_interface_details, InterfaceError
from core.vendor import generate_vendor_mac
from utils.logger import setup_logger, print_warning, print_success

logger = setup_logger(__name__)

# State file to store original MACs for restoration
STATE_FILE = os.path.expanduser("~/.mac_spoofer_state.json")

class SpooferError(Exception):
    """Custom exception for spoofing related errors."""
    pass

def generate_random_mac() -> str:
    """
    Generates a random valid MAC address.
    Ensures the address is unicast (least significant bit of first byte is 0).
    """
    # 02 for locally administered unicast
    mac = [0x02, 
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(f"{x:02x}" for x in mac)

def _save_original_mac(interface: str, mac: str) -> None:
    """Saves the original MAC address to a state file."""
    state = {}
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    # Only save if not already stored
    if interface not in state:
        state[interface] = mac
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)

def _get_saved_mac(interface: str) -> Optional[str]:
    """Retrieves the saved original MAC address."""
    if not os.path.exists(STATE_FILE):
        return None
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
            return state.get(interface)
    except (json.JSONDecodeError, IOError):
        return None

def change_mac(interface: str, new_mac: str) -> bool:
    """
    Changes the MAC address of the specified interface.
    """
    try:
        new_mac = normalize_mac(new_mac)
        details = get_interface_details(interface)
        current_mac = details["mac"]
        
        if current_mac == new_mac:
            logger.info(f"Interface {interface} already has MAC {new_mac}")
            return True

        # Warning for active interface
        if details["state"] == "UP" and details["ip"] != "None":
            print_warning(f"Interface {interface} is currently UP with IP {details['ip']}. Spoofing may drop your connection.")

        # Save current if it's the first time changing
        if current_mac and current_mac != "Unknown":
            _save_original_mac(interface, current_mac)

        logger.info(f"Changing MAC for {interface} from {current_mac} to {new_mac}")

        commands = [
            ["ip", "link", "set", "dev", interface, "down"],
            ["ip", "link", "set", "dev", interface, "address", new_mac],
            ["ip", "link", "set", "dev", interface, "up"]
        ]

        for cmd in commands:
            subprocess.check_call(cmd)
            
        updated_details = get_interface_details(interface)
        if updated_details["mac"] != new_mac:
            raise SpooferError(f"Verification failed: expected {new_mac}, got {updated_details['mac']}")

        return True

    except (MACValidationError, InterfaceError, subprocess.CalledProcessError) as e:
        logger.error(f"Failed to change MAC for {interface}: {e}")
        raise SpooferError(f"Spoofing failed: {e}")

def run_interval_mode(interface: str, interval_min: int, vendor: str = "random") -> None:
    """
    Runs a loop to change the MAC address every N minutes.
    """
    logger.info(f"Starting interval mode for {interface} (every {interval_min} minutes)")
    try:
        while True:
            new_mac = generate_vendor_mac(vendor)
            if change_mac(interface, new_mac):
                print_success(f"Interval Spoof: {interface} -> {new_mac}")
            time.sleep(interval_min * 60)
    except KeyboardInterrupt:
        logger.info("Interval mode stopped by user.")


def restore_mac(interface: str) -> bool:
    """Restores the original MAC address for the interface."""
    original_mac = _get_saved_mac(interface)
    if not original_mac:
        raise SpooferError(f"No original MAC address found for {interface} in state file.")
    
    logger.info(f"Restoring original MAC {original_mac} for {interface}")
    return change_mac(interface, original_mac)
