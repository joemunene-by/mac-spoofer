import re
from typing import Optional

class MACValidationError(Exception):
    """Custom exception for MAC address validation errors."""
    pass

def is_valid_mac(mac: str) -> bool:
    """
    Validates the format of a MAC address.
    
    Args:
        mac: The MAC address string to validate.
        
    Returns:
        True if valid, False otherwise.
    """
    # Regex for standard MAC address formats:
    # 00:11:22:33:44:55
    # 00-11-22-33-44-55
    # 0011.2233.4455
    pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$|^([0-9A-Fa-f]{4}\.){2}([0-9A-Fa-f]{4})$')
    return bool(pattern.match(mac))

def normalize_mac(mac: str) -> str:
    """
    Normalizes a MAC address to the format 00:11:22:33:44:55.
    
    Args:
        mac: The MAC address string to normalize.
        
    Returns:
        The normalized MAC address.
        
    Raises:
        MACValidationError: If the MAC address format is invalid.
    """
    if not is_valid_mac(mac):
        raise MACValidationError(f"Invalid MAC address format: {mac}")
    
    # Remove separators
    clean_mac = re.sub(r'[:.-]', '', mac).lower()
    
    # Format as 00:11:22:33:44:55
    return ':'.join(clean_mac[i:i+2] for i in range(0, 12, 2))
