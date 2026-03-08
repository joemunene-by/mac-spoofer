# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-09

### Added
- **Core Engine**: Implemented `core/spoofer.py` for MAC address modification on Linux interfaces.
- **Validation**: Added `core/validator.py` with strict regex-based MAC format validation and normalization.
- **Vendor Intelligence**: Integrated OUI database in `core/vendor.py` for spoofing as specific manufacturers (Samsung, Apple, Intel, etc.).
- **Profile System**: Created `core/profiles.py` to save and load named MAC configurations in `~/.mac-spoofer/profiles.json`.
- **Interface Detection**: Enhanced `core/interface.py` to detect IP addresses, connection states (UP/DOWN), and hardware types (WiFi/Ethernet).
- **Interactive TUI**: Added a menu-driven interactive mode in `cli/tui.py` using `rich`.
- **Daemon Mode**: Implemented `--interval` flag in `cli/main.py` for automated MAC rotation.
- **Stealth Mode**: Added `--stealth` flag to clear shell history after execution.
- **Persistence**: Provided `scripts/mac-spoofer@.service` for systemd-based persistence on boot.
- **Testing**: Built a comprehensive test suite in `tests/test_core.py` using `pytest`.
- **CI/CD**: Configured GitHub Actions in `.github/workflows/ci.yml` for automated linting (flake8), type checking (mypy), and testing.

### Changed
- **UI Design**: Refactored CLI output in `cli/main.py` and `utils/logger.py` to follow "Uncodixified" design principles (cleaner tables, minimal colors).
- **Tooling**: Switched to `pipx` as the recommended installation method.

### Fixed
- Resolved `ModuleNotFoundError` in CI by configuring `PYTHONPATH` in `.github/workflows/ci.yml`.
- Fixed `mypy` module resolution errors by adding `__init__.py` files and `mypy.ini` configuration.
- Corrected undefined names and missing imports in `cli/main.py` and `cli/tui.py`.
