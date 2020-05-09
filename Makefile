.PHONY: docs
docs:
	poetry export -f requirements.txt > docs/requirements.txt && \
	cd docs && \
	make html && \
	open _build/html/index.html

.PHONY: fmt
fmt:
	poetry run isort -y && \
	poetry run black .

.PHONY: setup
setup:
	brew install asdf || True
	asdf install
	poetry install
	poetry install --extras visual
