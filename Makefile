# shortcuts to help manage flipping between branches with different dependencies
sync:
	poetry install --extras dev --sync

update_lock_only:
	poetry update --lock

update: update_lock_only
	poetry install --extras dev

check:
	poetry check

requirements:
	poetry export --without-hashes --extras dev -f requirements.txt > requirements.txt

.PHONY: sync update_lock_only update check requirements

black-check:
	black --check .

black:
	black .

ruff:
	ruff .

mypy:
	mypy .

lint: ruff mypy

pre-check-in:
	make black-check
	make lint

.PHONY: black-check black ruff mypy lint pre-check-in
