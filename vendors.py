"""
vendors.py — Common OUI (Organizationally Unique Identifier) prefixes
mapped to vendor names. Used for realistic MAC address spoofing.

Each OUI is the first 3 octets of a MAC address assigned by IEEE to
a specific hardware manufacturer.
"""

# Mapping of vendor name (lowercase key) to a list of known OUI prefixes.
# Multiple OUIs per vendor increase variety when generating spoofed addresses.
VENDORS = {
    "apple": [
        "00:03:93", "00:05:02", "00:0A:27", "00:0D:93",
        "00:10:FA", "00:1C:B3", "00:1E:C2", "00:25:00",
        "3C:15:C2", "A4:B1:97", "F0:DB:E2",
    ],
    "samsung": [
        "00:07:AB", "00:12:FB", "00:15:99", "00:16:32",
        "00:21:19", "00:26:37", "34:C3:AC", "50:01:BB",
        "84:25:DB", "A8:06:00", "FC:A1:3E",
    ],
    "intel": [
        "00:02:B3", "00:03:47", "00:04:23", "00:0E:0C",
        "00:0E:35", "00:13:02", "00:13:20", "00:13:E8",
        "00:15:00", "00:15:17", "00:16:6F", "00:16:76",
        "00:18:DE", "00:1B:21", "00:1C:BF", "00:1E:64",
        "3C:97:0E", "68:05:CA", "8C:8D:28",
    ],
    "cisco": [
        "00:00:0C", "00:01:42", "00:01:43", "00:01:63",
        "00:01:64", "00:01:96", "00:01:97", "00:01:C7",
        "00:0B:BE", "00:0D:BC", "00:12:80", "00:18:73",
    ],
    "dell": [
        "00:06:5B", "00:08:74", "00:0B:DB", "00:0D:56",
        "00:0F:1F", "00:11:43", "00:12:3F", "00:13:72",
        "00:14:22", "00:15:C5", "00:18:8B", "00:1A:A0",
    ],
    "google": [
        "00:1A:11", "3C:5A:B4", "54:60:09", "94:EB:2C",
        "A4:77:33", "F4:F5:D8", "F8:8F:CA",
    ],
    "microsoft": [
        "00:0D:3A", "00:12:5A", "00:15:5D", "00:17:FA",
        "00:1D:D8", "00:22:48", "00:50:F2", "28:18:78",
        "7C:1E:52", "DC:B4:C4",
    ],
    "huawei": [
        "00:1E:10", "00:25:68", "00:25:9E", "00:34:FE",
        "00:46:4B", "00:E0:FC", "04:02:1F", "04:C0:6F",
        "20:08:ED", "24:09:95", "48:46:FB",
    ],
    "tp-link": [
        "00:27:19", "14:CC:20", "30:B5:C2", "50:C7:BF",
        "54:C8:0F", "60:E3:27", "90:F6:52", "A0:F3:C1",
        "C0:25:E9", "EC:08:6B", "F4:EC:38",
    ],
    "netgear": [
        "00:09:5B", "00:0F:B5", "00:14:6C", "00:1B:2F",
        "00:1E:2A", "00:1F:33", "00:24:B2", "00:26:F2",
        "20:0C:C8", "2C:B0:5D", "4C:60:DE",
    ],
    "sony": [
        "00:01:4A", "00:04:1F", "00:0A:D9", "00:0E:07",
        "00:12:EE", "00:13:A9", "00:15:C1", "00:1A:80",
        "00:1D:0D", "00:1E:A4", "00:24:8D",
    ],
    "lg": [
        "00:1C:62", "00:1E:75", "00:22:A9", "00:24:83",
        "00:26:E2", "00:34:DA", "00:AA:70", "10:68:3F",
        "20:3D:BD", "34:FC:EF", "40:B0:FA",
    ],
    "xiaomi": [
        "00:9E:C8", "04:CF:8C", "0C:1D:AF", "10:2A:B3",
        "14:F6:5A", "18:59:36", "28:6C:07", "34:80:B3",
        "50:64:2B", "58:44:98", "64:B4:73",
    ],
    "asus": [
        "00:0C:6E", "00:0E:A6", "00:11:2F", "00:11:D8",
        "00:13:D4", "00:15:F2", "00:17:31", "00:1A:92",
        "00:1D:60", "00:1E:8C", "00:22:15",
    ],
    "lenovo": [
        "00:06:1B", "00:09:2D", "00:12:FE", "00:1A:6B",
        "00:21:CC", "00:24:7E", "00:26:2D", "28:D2:44",
        "40:B0:34", "54:EE:75", "70:F1:A1",
    ],
    "hp": [
        "00:01:E6", "00:04:EA", "00:08:02", "00:0A:57",
        "00:0B:CD", "00:0D:9D", "00:0E:7F", "00:0F:20",
        "00:10:83", "00:11:0A", "00:12:79",
    ],
    "motorola": [
        "00:04:56", "00:08:0E", "00:0A:28", "00:0C:E5",
        "00:0E:5C", "00:0F:9F", "00:11:1A", "00:12:25",
        "00:14:04", "00:14:E8", "00:17:00",
    ],
    "nvidia": [
        "00:04:4B", "00:0D:61", "48:B0:2D", "54:AB:3A",
        "A4:BA:DB",
    ],
}


def get_vendor_names():
    """Return a sorted list of all available vendor names."""
    return sorted(VENDORS.keys())


def get_oui_for_vendor(vendor):
    """
    Return the list of OUI prefixes for the given vendor name.
    Case-insensitive lookup. Returns None if vendor is not found.
    """
    return VENDORS.get(vendor.lower())


def lookup_vendor_by_mac(mac):
    """
    Given a full MAC address string, return the vendor name if the OUI
    matches a known vendor, otherwise return None.
    """
    mac_upper = mac.upper().replace("-", ":")
    oui = mac_upper[:8]
    for vendor, ouis in VENDORS.items():
        if oui.upper() in [o.upper() for o in ouis]:
            return vendor.capitalize()
    return None
