test:
		uv run pytest -vvvrP

lint:
		uv run ruff check .

format:
		uv run ruff format .

checks:
		make lint
		make test