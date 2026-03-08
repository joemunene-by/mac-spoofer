├── cli/
│   ├── __init__.py
│   ├── main.py          # Entry point and CLI logic
│   └── tui.py           # Interactive menu system
├── core/
│   ├── __init__.py
│   ├── interface.py     # Interface management
│   ├── profiles.py      # Profile management
│   ├── spoofer.py       # Spoofing logic
│   ├── validator.py     # MAC validation
│   └── vendor.py        # OUI/Vendor database
├── utils/
│   ├── __init__.py
│   └── logger.py        # Logging configuration
├── scripts/
│   └── mac-spoofer@.service # Persistence
├── tests/
│   ├── __init__.py
│   └── test_core.py     # Unit tests
├── CHANGELOG.md         # Version history
├── RELEASE_NOTES.md     # Release summary
├── mypy.ini             # Type check config
├── Makefile             # Automation
└── setup.py             # Packaging
