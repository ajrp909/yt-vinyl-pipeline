install:
		uv sync
		uv pip install -e .

test:
		uv run pytest -vvvrP

lint:
		uv run ruff check .

format:
		uv run ruff format .

checks:
		make lint
		make test
pipeline:
		uv run src/yt_vinyl/pipeline.py