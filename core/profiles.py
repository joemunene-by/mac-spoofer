import os
import json
from typing import Dict, Optional, List
from core.validator import normalize_mac, MACValidationError
from utils.logger import setup_logger

logger = setup_logger(__name__)

CONFIG_DIR = os.path.expanduser("~/.mac-spoofer")
PROFILES_FILE = os.path.join(CONFIG_DIR, "profiles.json")

def _ensure_config_dir() -> None:
    """Ensures the configuration directory exists."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, mode=0o700)

def load_profiles() -> Dict[str, str]:
    """
    Loads saved MAC profiles from the config file.
    
    Returns:
        A dictionary of profile names and their MAC addresses.
    """
    if not os.path.exists(PROFILES_FILE):
        return {}
    
    try:
        with open(PROFILES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Failed to load profiles: {e}")
        return {}

def save_profile(name: str, mac: str) -> bool:
    """
    Saves a MAC address to a named profile.
    
    Args:
        name: The name of the profile.
        mac: The MAC address to save.
        
    Returns:
        True if successful, False otherwise.
    """
    try:
        mac = normalize_mac(mac)
        _ensure_config_dir()
        profiles = load_profiles()
        profiles[name] = mac
        
        with open(PROFILES_FILE, 'w') as f:
            json.dump(profiles, f, indent=4)
        return True
    except (MACValidationError, IOError) as e:
        logger.error(f"Failed to save profile {name}: {e}")
        return False

def get_profile_mac(name: str) -> Optional[str]:
    """Retrieves the MAC address for a given profile name."""
    profiles = load_profiles()
    return profiles.get(name)

def delete_profile(name: str) -> bool:
    """Deletes a named profile."""
    profiles = load_profiles()
    if name in profiles:
        del profiles[name]
        try:
            with open(PROFILES_FILE, 'w') as f:
                json.dump(profiles, f, indent=4)
            return True
        except IOError:
            return False
    return False

def list_profiles() -> List[str]:
    """Returns a list of all saved profile names."""
    return list(load_profiles().keys())
