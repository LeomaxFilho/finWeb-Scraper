"""Utilities para mineração de URLs e extração de texto de artigos HTML.

Este módulo fornece funções simples para baixar o conteúdo HTML de uma
URL e para extrair o texto limpo de um artigo HTML usando BeautifulSoup."""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from tqdm import tqdm

COLUMN_NUMBERS = 100


async def articles_fetch(urls: list[str]) -> list[str]:
    """Recebe a lista de urls para dar fetch e retorna uma lista os artigos"""

    async with asyncio.TaskGroup() as tg:
        task_list = [tg.create_task(fetch_url(article)) for article in urls]

    articles = [article.result() for article in tqdm(task_list)]

    return articles


async def fetch_url(url: str) -> str:
    """
    def fetch_url(url: str) -> str:

    Realiza uma requisição HTTP GET para a URL fornecida.

    Args:
        url (str): URL a ser acessada.

    Returns:
        str: Conteúdo HTML da resposta em caso de sucesso, ou 'Error' em caso de falha.
    """

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url, timeout=5) as request:
                request.raise_for_status()
                response = await request.text()

        except aiohttp.ClientResponseError as ex:
            print(f"\033[91m Response Error URL: {ex}\033[0m")
            return "Error"

        except aiohttp.InvalidURL as ex:
            print(f"\033[91m Invalid URL: {ex}\033[0m")
            return "Error"

        except aiohttp.ClientError as ex:
            print(f"\033[91m Client Error: {ex}\033[0m")
            return "Error"

    return response


async def soup_articles_fetch(articles: list[str]) -> list[str]:
    """Retorna um array com todos os artigos devidamente soupados"""
    async with asyncio.TaskGroup() as tg:
        task_group = [
            tg.create_task(soup_articles_html(article)) for article in articles
        ]
    articles_without_blank_spaces = [article.result() for article in task_group]

    return articles_without_blank_spaces


async def soup_articles_html(article: str) -> str:
    """
    def soup_articles_html (article: str) -> str:

    Extrai o texto limpo de um artigo HTML, removendo quebras de linha.

    Args:
        article (str): Conteúdo HTML do artigo.

    Returns:
        str: Texto do artigo sem quebras de linha.
    """
    soup = BeautifulSoup(article, "html.parser")
    soup_without_blank_lines = "".join(soup.text.splitlines())
    return soup_without_blank_lines
