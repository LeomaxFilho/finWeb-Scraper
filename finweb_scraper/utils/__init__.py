"""Módulo utilitário do pacote finweb_scraper.utils.

Este módulo reexporta funções úteis para mineração de URLs e extração
de texto de artigos HTML, provendo uma interface simples para uso
em outras partes do pacote ou por usuários.

Funções reexportadas:
- fetchUrl(url: str) -> str: realiza uma requisição HTTP GET e retorna o
        conteúdo HTML (ou a string 'Error' em caso de falha).
- soupArticlesHtml(article: str) -> str: transforma HTML em texto limpo,
        removendo quebras de linha.

Exemplo de uso:
                from finweb_scraper.utils import fetchUrl, soupArticlesHtml

                html = fetchUrl('https://exemplo.com')
                texto = soupArticlesHtml(html)
"""

# import fetch_url
from finweb_scraper.utils.async_requests import articles_fetch

# import soup_articles_html
from finweb_scraper.utils.async_requests import soup_articles_html
