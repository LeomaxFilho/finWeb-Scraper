"""Utilities para mineração de URLs e extração de texto de artigos HTML.

Este módulo fornece funções simples para baixar o conteúdo HTML de uma
URL e para extrair o texto limpo de um artigo HTML usando BeautifulSoup.

Funções públicas:
- fetch_url(url: str) -> str
    Realiza uma requisição HTTP GET e retorna o conteúdo HTML como string
    ou a string 'Error' em caso de resposta não-200.
- soup_articles_html(article: str) -> str
    Converte HTML em texto simples, removendo quebras de linha.

Exemplo de uso:
    from finweb_scraper.utils import urlmining

    html = urlmining.fetch_url('https://exemplo.com')
    texto = urlmining.soup_articles_html(html)

Observações:
- Os nomes das funções usam snake_case (ex.: fetch_url). Considere
  padronizá-los para PEP8 (fetch_url, soup_articles_html) se for necessário
  compatibilizar com outras partes do projeto.
"""

import sys
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def fetch_url(url: str) -> str:
    """
    def fetch_url(url: str) -> str:

    Realiza uma requisição HTTP GET para a URL fornecida.

    Args:
        url (str): URL a ser acessada.

    Returns:
        str: Conteúdo HTML da resposta em caso de sucesso, ou 'Error' em caso de falha.
    """
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.HTTPError as ex:
        print(f'\033[91m request error: {ex}\033[0m')
        sys.exit()
    except requests.exceptions.ConnectionError as ex:
        print(f'\033[91m request error: {ex}\033[0m')
        sys.exit()
    except requests.exceptions.Timeout as ex:
        print(f'\033[91m request error: {ex}\033[0m')
        sys.exit()

    if response.status_code != 200:
        tqdm.write(f'\033[91m error: {url}\033[0m')
        return 'Error'

    return response.text


def soup_articles_html (article: str) -> str:
    """
    def soup_articles_html (article: str) -> str:

    Extrai o texto limpo de um artigo HTML, removendo quebras de linha.

    Args:
        article (str): Conteúdo HTML do artigo.

    Returns:
        str: Texto do artigo sem quebras de linha.
    """
    soup = BeautifulSoup(article, 'html.parser')
    soup_without_blank_lines = ''.join(soup.text.splitlines())
    return soup_without_blank_lines
