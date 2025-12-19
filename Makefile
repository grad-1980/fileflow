.PHONY: help test run clean

help:
	@echo "Available commands:"
	@echo "  make test    - run pytest"
	@echo "  make run     - run fileflow CLI example"
	@echo "  make clean   - remove cache files"

test:
	pytest

run:
	python -m fileflow.cli run data/text_comd.txt --strip --drop-empty

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov