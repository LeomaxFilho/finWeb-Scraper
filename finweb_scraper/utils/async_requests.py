"""Asynchronous helpers for fetching article HTML and extracting text.

This module provides coroutine-based utilities to concurrently fetch HTML
from multiple URLs using aiohttp and to extract cleaned article text using
BeautifulSoup. The functions are intentionally simple and resilient: network
errors are caught and represented by the string "Error" for that item so the
caller can filter or handle failures.

Functions
- articles_fetch(urls: list[str]) -> list[str]
  Concurrently fetch multiple URLs and return their HTML contents (or "Error").

- fetch_url(url: str) -> str
  Fetch a single URL and return the response text, or "Error" on failure.

- soup_articles_fetch(articles: list[str]) -> list[str]
  Concurrently extract cleaned text from a list of HTML documents.

- soup_articles_html(article: str) -> str
  Extract cleaned text from a single HTML document.

Notes
- These coroutines use asyncio.TaskGroup (Python 3.11+) for concurrency.
- Network timeouts and common aiohttp exceptions are handled inside
  `fetch_url`; callers receive the literal string "Error" for failed fetches.
"""

import aiohttp
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm_asyncio
from tqdm import tqdm

COLUMN_NUMBERS = 100


async def articles_fetch(urls: list[str]) -> list[str]:
    """Concurrently fetch multiple URLs.

    This coroutine schedules concurrent fetches for each URL in `urls` and
    returns a list with the resulting HTML text for each URL. If a fetch
    fails for any reason the corresponding item in the returned list will be
    the string "Error".

    Args:
        urls: A list of URL strings to fetch.

    Returns:
        A list of strings where each element is the HTML content for the
        corresponding URL in `urls`, or the string "Error" for failed fetches.

    Notes:
        - Order of results matches the order of the input `urls` list.
        - Uses asyncio.TaskGroup (requires Python 3.11+).
        - A progress bar provided by `tqdm` displays while awaiting results.

    Example:
        >>> import asyncio
        >>> html_list = asyncio.run(articles_fetch(['https://example.com']))
    """

    async with aiohttp.ClientSession() as session:
        articles = await tqdm_asyncio.gather(
            *[fetch_url(article, session) for article in urls]
        )

    return articles


async def fetch_url(url: str, session: aiohttp.ClientSession) -> str:
    """Fetch a URL using aiohttp and return the response text.

    This coroutine performs an HTTP GET to the given `url` using an
    aiohttp.ClientSession. Common network and client errors are caught and
    logged to stdout; on failure the function returns the string "Error".

    Args:
        url: The URL to request.

    Returns:
        The response body as text when the request succeeds, or the string
        "Error" when the request fails (for example, invalid URL, timeout,
        non-2xx response, or other client errors).

    Implementation details:
        - Uses a 5 second timeout for the request.
        - Catches `aiohttp.ClientResponseError`, `aiohttp.InvalidURL`, and
          `aiohttp.ClientError` and returns "Error" for those cases.

    Example:
        >>> import asyncio
        >>> html = asyncio.run(fetch_url('https://example.com'))
    """

    try:
        async with session.get(url=url, timeout=5) as request:
            request.raise_for_status()
            response = await request.text()

    except aiohttp.ClientResponseError as ex:
        tqdm.write(f'\033[91m Response Error URL: {ex}\033[0m')
        return 'Error'

    except aiohttp.InvalidURL as ex:
        tqdm.write(f'\033[91m Invalid URL: {ex}\033[0m')
        return 'Error'

    except aiohttp.ConnectionTimeoutError as ex:
        tqdm.write(f'\033[91m Timeout Error: {ex}\033[0m')
        return 'Error'

    except aiohttp.ClientError as ex:
        tqdm.write(f'\033[91m Client Error: {ex}\033[0m')
        return 'Error'

    return response


async def soup_articles_fetch(articles: list[str]) -> list[str]:
    """Concurrently extract article text from multiple HTML documents.

    Schedules `soup_articles_html` for each item in `articles` and returns a
    list of cleaned article text strings. If an input item is not valid HTML
    or is the string "Error" (e.g. a failed fetch), the corresponding output
    will be the result of parsing that input (often an empty string or the
    literal "Error" passed through).

    Args:
        articles: A list of HTML document strings.

    Returns:
        A list of cleaned article text strings, in the same order as the
        input `articles`.
    """

    articles_without_blank_spaces = await tqdm_asyncio.gather(
        *[soup_articles_html(article) for article in articles]
    )

    return articles_without_blank_spaces


async def soup_articles_html(article: str) -> str:
    """Extract cleaned text from a single HTML document.

    The function parses the supplied HTML string with BeautifulSoup and
    returns the visible text with all line breaks removed. This is useful as
    a simple, fast way to get contiguous article text, but it does not
    attempt advanced boilerplate removal.

    Args:
        article: HTML document as a string.

    Returns:
        A string with the extracted text where line breaks have been removed.

    Example:
        >>> import asyncio
        >>> text = asyncio.run(soup_articles_html('<html><body>Hi\nthere</body></html>'))
        >>> tqdm.write(text)
        'Hithere'
    """

    soup = BeautifulSoup(article, 'html.parser')
    soup_without_blank_lines = ''.join(soup.text.splitlines())

    return soup_without_blank_lines
