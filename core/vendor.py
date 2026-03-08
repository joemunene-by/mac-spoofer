import random
from typing import Dict, Optional, List

# A curated list of popular OUIs for common vendors
# Format: {Vendor: [OUI_Prefixes]}
VENDOR_OUIS: Dict[str, List[str]] = {
    "Apple": ["00:03:93", "00:05:02", "00:0a:27", "00:0a:95", "00:0d:93", "00:10:fa"],
    "Samsung": ["00:00:f0", "00:07:ab", "00:0d:e6", "00:12:47", "00:15:b9", "00:16:32"],
    "Google": ["00:1a:11", "3c:5a:b4", "d8:eb:46", "f4:f5:d8"],
    "Intel": ["00:02:b3", "00:03:47", "00:04:23", "00:07:e9", "00:08:ca", "00:0c:f1"],
    "Cisco": ["00:00:0c", "00:01:42", "00:01:43", "00:01:63", "00:01:64", "00:01:96"],
    "Dell": ["00:06:5b", "00:08:74", "00:0a:e4", "00:0b:db", "00:0d:56", "00:0f:1f"],
    "HP": ["00:01:e6", "00:0b:cd", "00:0d:9d", "00:0e:7f", "00:0f:20", "00:10:83"],
    "Microsoft": ["00:03:ff", "00:12:5a", "00:15:5d", "00:17:fa", "00:1d:d8", "00:22:48"],
}

def get_vendor_from_mac(mac: str) -> str:
    """
    Identifies the vendor based on the MAC address OUI.
    
    Args:
        mac: The MAC address string.
        
    Returns:
        The vendor name or 'Unknown'.
    """
    if not mac or mac == "Unknown":
        return "Unknown"
    
    oui = mac.upper()[:8].replace("-", ":")
    for vendor, prefixes in VENDOR_OUIS.items():
        if any(oui == p.upper() for p in prefixes):
            return vendor
    return "Unknown"

def generate_vendor_mac(vendor: str = "random") -> str:
    """
    Generates a MAC address for a specific vendor or a random one from the list.
    
    Args:
        vendor: The vendor name or 'random'.
        
    Returns:
        A valid MAC address string.
    """
    if vendor.lower() == "random":
        vendor = random.choice(list(VENDOR_OUIS.keys()))
    
    prefixes = VENDOR_OUIS.get(vendor.capitalize())
    if not prefixes:
        # Fallback to random if vendor not found
        prefixes = random.choice(list(VENDOR_OUIS.values()))
    
    prefix = random.choice(prefixes)
    suffix = ":".join(f"{random.randint(0x00, 0xff):02x}" for _ in range(3))
    return f"{prefix}:{suffix}".lower()

def list_vendors() -> List[str]:
    """Returns a list of supported vendors."""
    return list(VENDOR_OUIS.keys())
