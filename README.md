# finWeb-Scraper
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FLeomaxFilho%2FfinWeb-Scraper.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FLeomaxFilho%2FfinWeb-Scraper?ref=badge_shield)


## What is this?

finWeb-Scraper is a small Python utility to collect news article metadata from the NewsAPI, fetch each article's HTML, extract the article text using BeautifulSoup, and optionally send the cleaned article text to a local Ollama instance for further processing. The project produces JSON output files that store the raw API response, the cleaned article text, and (if used) the AI responses.

This repository is intended as a lightweight starting point for building pipelines that need to harvest news content and post-process it locally.

## Features

- Query NewsAPI for articles (the script uses the `everything` endpoint).
- Download each article URL and extract readable text with BeautifulSoup.
- Optional post-processing step that calls a local Ollama HTTP API to transform or clean the article text.
- Progress reporting using `tqdm`.

## Requirements

- Python 3.9+ (recommended: 3.11)
- The script depends on the following Python packages:
  - requests
  - beautifulsoup4
  - python-dotenv
  - tqdm

If you keep a `pyproject.toml` in the repository you can also use `pip install -e .` or any dependency management tool you prefer.

## Configuration / Environment variables

The script reads configuration from environment variables. To make local development convenient, you can add a `.env` file at the project root with the following variables:

- API_NEWSAPI: Your NewsAPI API key (required to query NewsAPI).
- URL_OLLAMA: (optional) Local Ollama HTTP API URL (default used in the script: `http://localhost:11434/api/generate`).
- OLLA_MODEL: (optional) Ollama model identifier to use when calling the local Ollama instance.

Example `.env`:

```env
API_NEWSAPI=sk_your_newsapi_key_here
URL_OLLAMA=http://localhost:11434/api/generate
OLLA_MODEL=llama3.2:latest
```

Note: The NewsAPI key is required to fetch the list of articles. The Ollama settings are optional — the script will attempt to call Ollama only if you have a local Ollama server running and the script is configured to do so.

## How to run

1. Ensure you have the dependencies installed and the `.env` file created (or environment variables exported).

3. Run the main script:

```zsh
python finweb_scraper/news.py
```

The script currently uses a hard-coded query parameter (`'q': 'Petrobras'`) and language `'pt'` in the main block. Modify `finweb_scraper/news.py` if you want to change the default query or other parameters.

## What the script writes

After a successful run you will find these files in the `out/` directory:

- `out.json` — The full JSON response returned by NewsAPI.
- `articles.json` — An array of the extracted article texts (HTML fetched and cleaned with BeautifulSoup).
- `response.json` — If the Ollama API is called, this will contain the JSON responses from the Ollama model for each article.

## License

This project is provided as-is. Check the `LICENSE` file in the repository for the project's license.

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FLeomaxFilho%2FfinWeb-Scraper.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FLeomaxFilho%2FfinWeb-Scraper?ref=badge_large)