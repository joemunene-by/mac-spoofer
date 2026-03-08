import pytest
from core.validator import is_valid_mac, normalize_mac, MACValidationError
from core.spoofer import generate_random_mac
from core.vendor import generate_vendor_mac, get_vendor_from_mac
from core.profiles import save_profile, get_profile_mac, delete_profile

def test_mac_validation():
    assert is_valid_mac("00:11:22:33:44:55") == True
    assert is_valid_mac("00-11-22-33-44-55") == True
    assert is_valid_mac("0011.2233.4455") == True
    assert is_valid_mac("invalid") == False
    assert is_valid_mac("00:11:22:33:44") == False

def test_mac_normalization():
    assert normalize_mac("00-11-22-33-44-55") == "00:11:22:33:44:55"
    assert normalize_mac("0011.2233.4455") == "00:11:22:33:44:55"
    with pytest.raises(MACValidationError):
        normalize_mac("invalid")

def test_random_mac_generation():
    mac = generate_random_mac()
    assert is_valid_mac(mac) == True
    # Check if locally administered unicast
    first_byte = int(mac.split(':')[0], 16)
    assert first_byte & 1 == 0

def test_vendor_mac_generation():
    mac = generate_vendor_mac("Samsung")
    assert is_valid_mac(mac) == True
    assert get_vendor_from_mac(mac) == "Samsung"

def test_profile_manager(tmp_path):
    # Mock profile file path if needed, but here we test the logic
    name = "test_profile"
    mac = "00:aa:bb:cc:dd:ee"
    assert save_profile(name, mac) == True
    assert get_profile_mac(name) == mac
    assert delete_profile(name) == True
    assert get_profile_mac(name) == None
