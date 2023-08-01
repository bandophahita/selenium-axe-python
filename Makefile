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

black:
	black .

ruff:
	ruff .

mypy:
	mypy .

lint: ruff mypy

test:
	python3 -m pytest ./selenium_axe_python/tests/

pre-check-in: black-check lint test

.PHONY: black-check black ruff mypy lint test pre-check-in

axe-core-update:
	python3 update_axe_core.py

.PHONY: axe-core-update
