# Code style checking
ruff:
	ruff check && ruff format --diff

# Fix code format
format:
	ruff check --fix && ruff format

# Static type checking
mypy:
	mypy .

# Pytest
pytest:
	pytest --doctest-modules

# Combined checking
check: format mypy pytest