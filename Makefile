.PHONY: help clean install dev-install test lint format build publish-test publish install-dev-deps fix-lint

# Variables
PYTHON = python3
PIP = pip
UV = uv
PKG_NAME = adktools
BUILD_DIR = dist
DEV_DEPS = black isort flake8 mypy pytest build twine

help:
	@echo "Available commands:"
	@echo "  make help             - Show this help message"
	@echo "  make clean            - Remove build artifacts and cache directories"
	@echo "  make install          - Install the package"
	@echo "  make dev-install      - Install the package in development mode with dev dependencies"
	@echo "  make install-dev-deps - Install development dependencies"
	@echo "  make test             - Run tests"
	@echo "  make lint             - Run linting checks"
	@echo "  make format           - Format code with Black and isort"
	@echo "  make fix-lint         - Fix linting issues automatically where possible"
	@echo "  make build            - Build the package"
	@echo "  make publish-test     - Publish package to TestPyPI"
	@echo "  make publish          - Publish package to PyPI"

clean:
	rm -rf $(BUILD_DIR) *.egg-info .coverage .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

install-dev-deps:
	$(PIP) install $(DEV_DEPS)

install:
	$(PIP) install .

dev-install: install-dev-deps
	$(PIP) install -e ".[dev]"

test:
	pytest

lint: install-dev-deps
	flake8 src tests
	mypy src tests
	black --check src tests
	isort --check src tests

format: install-dev-deps
	black src tests
	isort src tests

fix-lint: format
	# Remove unused imports
	autoflake --remove-all-unused-imports --recursive --in-place src tests

build: clean install-dev-deps
	$(PYTHON) -m build

publish-test: build
	$(PYTHON) -m twine upload --repository testpypi $(BUILD_DIR)/*

publish: build
	$(PYTHON) -m twine upload $(BUILD_DIR)/*

# UV-specific commands
uv-install-dev-deps:
	$(UV) pip install $(DEV_DEPS)

uv-install:
	$(UV) pip install .

uv-dev-install: uv-install-dev-deps
	$(UV) pip install -e ".[dev]"

uv-test: uv-install-dev-deps
	$(UV) run pytest

uv-lint: uv-install-dev-deps
	$(UV) run flake8 src tests
	$(UV) run mypy src tests
	$(UV) run black --check src tests
	$(UV) run isort --check src tests

uv-format: uv-install-dev-deps
	$(UV) run black src tests
	$(UV) run isort src tests

uv-fix-lint: uv-format
	$(UV) pip install autoflake
	$(UV) run autoflake --remove-all-unused-imports --recursive --in-place src tests

uv-build: clean uv-install-dev-deps
	$(UV) run build

uv-publish-test: uv-build
	$(UV) run twine upload --repository testpypi $(BUILD_DIR)/*

uv-publish: uv-build
	$(UV) run twine upload $(BUILD_DIR)/*