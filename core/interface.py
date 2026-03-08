import os
import subprocess
import platform
import re
import socket
from typing import List, Dict, Optional
from utils.logger import setup_logger
from core.vendor import get_vendor_from_mac

logger = setup_logger(__name__)

class InterfaceError(Exception):
    """Custom exception for network interface related errors."""
    pass

def get_interfaces() -> List[str]:
    """
    Retrieves a list of available network interfaces.
    Currently supports Linux.
    """
    if platform.system() != "Linux":
        raise InterfaceError(f"Operating system {platform.system()} is not supported.")

    try:
        interfaces = os.listdir('/sys/class/net')
        return [iface for iface in interfaces if iface != 'lo']
    except Exception as e:
        logger.error(f"Failed to list network interfaces: {e}")
        raise InterfaceError(f"Could not retrieve network interfaces: {e}")

def get_interface_details(interface: str) -> Dict[str, str]:
    """
    Retrieves detailed information about an interface.
    """
    details = {
        "interface": interface,
        "mac": "Unknown",
        "vendor": "Unknown",
        "state": "DOWN",
        "type": "Ethernet",
        "ip": "None"
    }

    try:
        # Get MAC and State using ip link
        ip_link_output = subprocess.check_output(["ip", "link", "show", interface]).decode("utf-8")
        
        mac_match = re.search(r"link/ether\s+([0-9a-fA-F:]{17})", ip_link_output)
        if mac_match:
            details["mac"] = mac_match.group(1)
            details["vendor"] = get_vendor_from_mac(details["mac"])

        if "state UP" in ip_link_output:
            details["state"] = "UP"

        # Determine type (simple heuristic)
        if os.path.exists(f"/sys/class/net/{interface}/wireless"):
            details["type"] = "WiFi"
        
        # Get IP using ip addr
        ip_addr_output = subprocess.check_output(["ip", "addr", "show", interface]).decode("utf-8")
        ip_match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", ip_addr_output)
        if ip_match:
            details["ip"] = ip_match.group(1)

    except (subprocess.CalledProcessError, Exception) as e:
        logger.warning(f"Error getting details for {interface}: {e}")

    return details

def list_interfaces_with_details() -> List[Dict[str, str]]:
    """
    Returns a list of detailed interface information.
    """
    interfaces = get_interfaces()
    return [get_interface_details(iface) for iface in interfaces]

