INSTALL_DIR = /usr/local/bin
SERVICE_DIR = /etc/systemd/system

install:
	pip install .
	cp scripts/mac-spoofer@.service $(SERVICE_DIR)/

test:
	pytest tests/ --cov=core --cov=utils

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	mypy . --ignore-missing-imports

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: install test lint clean
