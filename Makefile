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
	poetry export --without-hashes -f requirements.txt > requirements.txt

.PHONY: sync update_lock_only update check requirements
