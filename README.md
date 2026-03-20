# yt-vinyl-pipeline

> The current state of the project is that it is a fully functional pipeline with a bronze ingestion layer, a silver layer, atomicity and a thoughtful test suite. I have further ideas to solve my own problems but recognise this can be built in a further customisable way for someone with a similar problem to adapt it to their needs. The transform interface is currently being refactored to give users a cleaner entry point. The quick start instructions will be updated when that is complete.

## What it is

For DJ sets, compilations or any structured music that have individual tracks in the description as long as they exist in a playlist somewhere, you can use this tool. It extracts the tracklist via the YouTube API, processes it, and produces a table of clean entries for each track, the artist and the source video ID they were extracted from. Then, you are free to do whatever you want with the data it spits out.

## Installation
```
git clone https://github.com/your-username/yt-vinyl-pipeline.git
cd yt-vinyl-pipeline
uv sync
uv pip install -e .
```

## Quick start

Obtain the playlist ID string that you want to parse into individual tracks. This is the `list=` parameter in the YouTube playlist URL.

Then, go to GCP and obtain an API key for the YouTube Data API v3 (enable the YouTube Data API v3 in the API library, then restrict the key to that API only for least privilege).

When in the root of the project, run `touch .env` and add the following:
```
YOUTUBE_API_KEY=your_key_here
PLAYLIST_ID=your_playlist_id_here
```

Once that is done, run `make pipeline` in the terminal and the pipeline should execute.

When the pipeline completes, your data lands in `videos.db` in the data directory. You can query it directly with any SQLite client.

## Writing your own transform

Navigate to `silver_transform` in the transform module and replace the parsing logic with your own. The output must be a list of dicts in this format:
```python
{"artist": "Artist Name", "track": "Track Title", "video_id": "video_id"}
```

The default implementation works for descriptions formatted as:
```
01 - Artist - Track Title
02 - Artist - Track Title
```

Replace or adapt the logic for your own format. It can be as simple or as complex as you require, a regex, a custom function, an LLM. It is only dependent in its current state on YouTube being the source and a structured output schema.

## Why it is built this way

The interesting part of this project is that the parsing logic is customisable by the user. There are strict requirements the pipeline has, it requires an output of video_id, artist and track to load the silver layer. This means it can be as complex as you require, it can involve many different formats, a function, a lambda, an LLM.

SQLite is the storage facility of choice, mainly due to it being lightweight for the volume that intended its initial use, but also because it is easily migrated to something more robust if the time came to it. The initial plan was not to build something with others in mind, but it developed into that after a revelation that this was widely applicable to others in a similar situation.

A medallion architecture was used where all raw playlist data is ingested, then transformed downstream. This ensures a video does not get processed more than once as a processed_date flag exists, which is null upon ingestion and becomes populated after the data has moved downstream. Each video is committed atomically. If a video fails halfway through, the record stays unprocessed in bronze ready to be picked up next time.

This was the first project where I set up with uv rather than traditionally using pip. Pre-commit hooks, ruff and pytest were used alongside a CI/CD pipeline in GitHub Actions. I wanted to build this simple project in a robust fashion in the way I was trained and feels natural to me.

Human intervention for this pipeline is paramount. You may not want every track from the description to move downstream, but it is important it exists in bronze and silver so it does not get reprocessed and you do not have to review the same thing again.
