# finweb-scraper (v0.1.0)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FLeomaxFilho%2FfinWeb-Scraper.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FLeomaxFilho%2FfinWeb-Scraper?ref=badge_shield)

Stock Market web scraper — a lightweight pipeline to harvest news articles, clean the HTML, and optionally post-process text with a local Ollama instance.

## Summary

This project queries NewsAPI for news about a topic, downloads the article HTML pages, extracts the article text using BeautifulSoup, and can forward the cleaned text to a local Ollama API for additional processing. It is intended as a simple, local-first scraper for building data pipelines around financial news.

## Project metadata

- Name: finweb-scraper
- Version: 0.1.0
- Description: Stock Market web scraper
- Authors: LeomaxFilho <leomax.filho@gmail.com>
- License: MIT
- Python: >=3.11

## Dependencies

The project declares the following runtime dependencies (as in `pyproject.toml`):

- requests (>=2.32.5,<3.0.0)
- tqdm (>=4.67.1,<5.0.0)
- dotenv (>=0.9.9,<0.10.0)
- beautifulsoup4 (>=4.14.2,<5.0.0)
- aiohttp (>=3.13.0,<4.0.0)

For testing (optional):

- pytest (>=8.4.2,<9.0.0)

## Installation

Using pip (recommended, example with virtualenv):

```zsh
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

Using Poetry (if you prefer to manage with `pyproject.toml`):

```zsh
poetry install
```

Note: the pins above are examples matching the lower-bound versions in `pyproject.toml`; you can adjust them to the exact versions you prefer.

## Configuration

Create a `.env` file at the repository root or export these environment variables before running the script:

- API_NEWSAPI — your NewsAPI API key (required to fetch articles)
- URL_OLLAMA — (optional) local Ollama API URL (default in the script: `http://localhost:11434/api/generate`)
- OLLA_MODEL — (optional) model id for Ollama (example: `llama3.2:latest`)

Example `.env`:

```env
API_NEWSAPI=sk_your_newsapi_key_here
URL_OLLAMA=http://localhost:11434/api/generate
OLLA_MODEL=llama3.2:latest
```

## Usage

1. Ensure dependencies are installed and `.env` is configured.
2. Create the `out/` directory where the script writes JSON files:

```zsh
mkdir -p out
```

3. Run the main script:

```zsh
python finweb_scraper/news.py
```

The script's default query in `finweb_scraper/news.py` is currently set to fetch articles about `Petrobras` and uses language `pt`. Edit the script to change the query or adapt it to accept command-line arguments.

## Output

The script writes JSON output files to the `out/` directory:

- `out.json` — raw JSON response from NewsAPI
- `articles.json` — list of cleaned article text (HTML fetched and cleaned)
- `response.json` — JSON responses from the Ollama API (if called)

## Development

- Code lives under `finweb_scraper/`. Key files:
  - `finweb_scraper/news.py` — main scraper script
  - `finweb_scraper/utils/async_requests.py` — asynchronous fetching and HTML-to-text helpers
## License

This project is licensed under the MIT License — see `LICENSE` for details.

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FLeomaxFilho%2FfinWeb-Scraper.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FLeomaxFilho%2FfinWeb-Scraper?ref=badge_large)
