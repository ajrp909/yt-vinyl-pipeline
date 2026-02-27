test:
		uv run pytest

lint:
		uv run ruff check .

format:
		uv run ruff format .

checks:
		make lint
		make test