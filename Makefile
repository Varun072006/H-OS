.PHONY: help install lint format typecheck test test-cov clean

help:
	@echo "HumanOS Development Commands:"
	@echo "  install    Install project dependencies in editable mode with dev options"
	@echo "  lint       Run Ruff linting"
	@echo "  format     Format code using Ruff"
	@echo "  typecheck  Run MyPy type checks"
	@echo "  test       Run unit tests"
	@echo "  test-cov   Run tests with coverage report"
	@echo "  clean      Remove build artifacts and cache directories"

install:
	pip install --upgrade pip setuptools wheel
	pip install -e ".[dev,ai]"

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy .

test:
	pytest

test-cov:
	pytest --cov=ai --cov=backend --cov=privacy --cov=streaming --cov-report=term-missing

clean:
	rm -rf build/ dist/ *.egg-info .mypy_cache .pytest_cache .ruff_cache htmlcov .coverage
