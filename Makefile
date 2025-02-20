# shortcuts to help manage flipping between branches with different dependencies
sync:
	poetry install --extras dev --sync

update-lock-only:
	poetry update --lock

update: update-lock-only
	poetry install --extras dev

check:
	poetry check

requirements:
	poetry export --without-hashes --extras dev -f requirements.txt > requirements.txt

.PHONY: sync update-lock-only update check requirements

black-check:
	black --check .

black-fix:
	black .

ruff-check:
	ruff check .

ruff-fix:
	ruff check . --fix --show-fixes

mypy:
	mypy .

lint: ruff-check mypy

test:
	python3 -m pytest ./selenium_axe_python/tests/

pre-check-in: black-check ruff-check mypy

pre-check-in-fix: black-fix ruff-fix mypy

.PHONY: black-check black ruff mypy lint test pre-check-in pre-check-in-fix

axe-core-update:
	python3 update_axe_core.py

.PHONY: axe-core-update

local_setup_selenium:
	pip uninstall setup-selenium-testing -y
	pip install -e ~/projects/setup_selenium

.PHONY: local_setup_selenium