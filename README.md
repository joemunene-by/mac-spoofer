![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux-informational?style=flat-square&logo=linux)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

# MAC Address Spoofer

A clean, Linux-focused CLI tool for viewing, spoofing, and restoring MAC
addresses on network interfaces. Supports random generation, vendor-specific
OUI spoofing (Apple, Samsung, Intel, and more), and interface management
through standard `ip link` commands.

## Features

- Show the current MAC address for any interface
- Generate a fully random, locally-administered MAC address
- Set an explicit MAC address of your choosing
- Spoof with a real vendor OUI for realistic device impersonation
- Restore the original MAC address saved before the first change
- List all network interfaces with MAC, state, and vendor info
- Validate MAC address format before applying
- Coloured terminal output (optional, via colorama)
- Graceful error handling when not running as root

## Supported Vendors

The following vendors are available for OUI-based spoofing (18 vendors,
100+ OUI prefixes):

| Vendor     | OUIs | Vendor     | OUIs |
|------------|------|------------|------|
| Apple      | 11   | Samsung    | 11   |
| Intel      | 19   | Cisco      | 12   |
| Dell       | 12   | Google     | 7    |
| Microsoft  | 10   | Huawei     | 11   |
| TP-Link    | 11   | Netgear    | 11   |
| Sony       | 11   | LG         | 11   |
| Xiaomi     | 11   | ASUS       | 11   |
| Lenovo     | 11   | HP         | 11   |
| Motorola   | 11   | NVIDIA     | 5    |

## Installation

```bash
git clone https://github.com/joemunene-by/mac-spoofer.git
cd mac-spoofer
pip install -r requirements.txt
```

colorama is the only external dependency and is optional -- the tool works
without it (you just lose coloured output).

## Usage

All commands that modify a MAC address require **root / sudo**.

### List all interfaces

```bash
python3 spoofer.py --list
```

```
Interface        MAC Address          State      Vendor
-----------------------------------------------------------------
eth0             08:00:27:a3:b4:c5    UP         
lo               00:00:00:00:00:00    UNKNOWN    
wlan0            00:15:af:33:21:bb    DOWN       Intel
```

### Show current MAC for an interface

```bash
python3 spoofer.py --interface eth0 --show
```

### Spoof with a random MAC

```bash
sudo python3 spoofer.py --interface eth0 --random
```

### Spoof with a vendor OUI

```bash
sudo python3 spoofer.py --interface wlan0 --vendor apple
```

### Set a specific MAC address

```bash
sudo python3 spoofer.py --interface eth0 --mac AA:BB:CC:DD:EE:FF
```

### Restore the original MAC

```bash
sudo python3 spoofer.py --interface eth0 --restore
```

### List available vendors

```bash
python3 spoofer.py --vendors
```

## Short Flags

| Long           | Short | Description                          |
|----------------|-------|--------------------------------------|
| `--interface`  | `-i`  | Target network interface             |
| `--random`     | `-r`  | Random locally-administered MAC      |
| `--mac`        | `-m`  | Explicit MAC address                 |
| `--vendor`     | `-v`  | Vendor name for OUI spoofing         |
| `--list`       | `-l`  | List all interfaces                  |
| `--show`       | `-s`  | Show MAC for the given interface     |
| `--restore`    |       | Restore original MAC                 |
| `--vendors`    |       | Print supported vendor names         |

## How It Works

1. The current MAC is read from `/sys/class/net/<iface>/address`.
2. Before the first change the original MAC is saved to a temp file so it
   can be restored later (even across separate invocations).
3. The interface is brought down with `ip link set dev <iface> down`.
4. The new MAC is applied with `ip link set dev <iface> address <mac>`.
5. The interface is brought back up.
6. The new address is verified by re-reading from `/sys`.

## Project Structure

```
mac-spoofer/
  spoofer.py        Main CLI entry point
  vendors.py        OUI-to-vendor mapping (18 vendors, 100+ prefixes)
  requirements.txt  Python dependencies (colorama)
  README.md         This file
  LICENSE           MIT license
```

## Disclaimer

This tool is provided for **educational and authorized testing purposes only**.

- Only use this tool on networks and hardware you own or have explicit
  written permission to test.
- Unauthorized MAC address spoofing may violate local, state, or federal
  laws, as well as your network provider's terms of service.
- The authors assume no liability for misuse of this software.

Use responsibly.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
details.
