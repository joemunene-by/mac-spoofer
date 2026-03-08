![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Linux-informational?style=flat-square&logo=linux)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![CI](https://github.com/joemunene-by/mac-spoofer/actions/workflows/ci.yml/badge.svg)
![Stars](https://img.shields.io/github/stars/joemunene-by/mac-spoofer?style=flat-square)
![Issues](https://img.shields.io/github/issues/joemunene-by/mac-spoofer?style=flat-square)
```

---

# MAC Address Spoofer CLI

![CI](https://github.com/joemunene-by/mac-address-spoofer/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey)

A professional, production-ready CLI tool for spoofing MAC addresses on Linux network interfaces.

## Advanced Features

- **Vendor Intelligence**: Spoof MACs from Apple, Samsung, Google, Intel, and more.
- **Persistence**: Auto-spoof on boot via systemd service.
- **Profiles**: Save and load custom MAC profiles.
- **Interval Mode**: Rotate MAC addresses automatically every N minutes.
- **Interactive TUI**: A guided terminal interface for ease of use.
- **Stealth Mode**: Clear shell history after execution.

## Installation

### pipx (Recommended)
```bash
pipx install git+https://github.com/joemunene-by/mac-address-spoofer.git
```

### From Source
```bash
git clone https://github.com/joemunene-by/mac-address-spoofer.git
cd mac-address-spoofer
make install
```

## Advanced Usage

### Interval Rotation
```bash
sudo mac-spoofer -i eth0 --interval 30 --vendor Apple
```

### Save/Load Profiles
```bash
sudo mac-spoofer -i eth0 --save-profile home
sudo mac-spoofer -i eth0 --load-profile home
```

### Systemd Persistence
```bash
sudo systemctl enable mac-spoofer@eth0
sudo systemctl start mac-spoofer@eth0
```

### Stealth Mode
```bash
sudo mac-spoofer -i eth0 -r --stealth --silent
```

## Project Structure

```text
├── cli/
│   └── main.py          # Entry point and CLI logic
├── core/
│   ├── interface.py     # Interface management
│   ├── spoofer.py       # Spoofing logic
│   └── validator.py     # MAC validation
├── utils/
│   └── logger.py        # Logging configuration
├── DISCLAIMER.md        # Ethical usage notice
├── LICENSE              # MIT License
├── README.md            # Documentation
└── setup.py             # Packaging
```

## Project Structure

See [STRUCTURE.md](STRUCTURE.md) for a full file breakdown.

## Ethics & Legality

Please refer to [DISCLAIMER.md](DISCLAIMER.md) for full details. Use this tool only on hardware you own or have explicit permission to test.
ok Interval Spoof: eth0 -> 00:0a:27:88:11:cc
...
```

### Profile Management
```text
$ sudo mac-spoofer -i eth0 --save-profile office
ok Profile 'office' saved: 00:0c:29:4f:89:1a

$ sudo mac-spoofer -i eth0 --load-profile office
ok Profile 'office' applied to eth0
```

### Interactive Menu
```text
$ sudo mac-spoofer
MAC Address Spoofer - Menu

Interface   Type       State   IP            MAC                 Vendor
eth0        Ethernet   UP      192.168.1.5   00:07:ab:44:92:ef   Samsung

1. Spoof Interface (Random)
2. Spoof Interface (Vendor)
3. Restore Original MAC
4. Load Profile
5. Quit

Select an option: _
```

## Ethics & Legality

Please refer to [DISCLAIMER.md](DISCLAIMER.md) for full details. Use this tool only on hardware you own or have explicit permission to test.
