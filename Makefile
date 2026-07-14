.PHONY: validate test check install-codex install-claude

validate:
	python scripts/validate_repo.py

test:
	python -m unittest discover -s tests -v

check: validate test

install-codex:
	python scripts/install.py --client codex --scope repo --mode copy

install-claude:
	python scripts/install.py --client claude-code --scope repo --mode copy
