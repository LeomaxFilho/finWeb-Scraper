"""Este módulo realiza operações de scraping de notícias financeiras 
    usando requests e BeautifulSoup.

Contém funções para buscar notícias, salvar resultados em arquivos e manipular URLs. 
Dependências externas: requests, tqdm, dotenv.

Uso:
    python news.py

"""

import sys
import os
import json
import requests
from tqdm import tqdm
from dotenv import load_dotenv
from .utils import fetch_Url, soup_Articles_Html

COLUMN_NUMBERS = 100

if __name__ == '__main__':
    load_dotenv()

    API_NEWSAPI=os.getenv('API_NEWSAPI')
    URL_NEWSAPI='https://newsapi.org/v2/everything'
    URL_OLLAMA='http://localhost:11434/api/generate'
    OLLA_MODEL='llama3.2:latest'

    paramNewsAPI = {
        'apiKey' : API_NEWSAPI,
        'q' : 'Petrobras',
        'searchIn' : 'title,content',
        'language' : 'pt',
    }

    try:
        response = requests.get(url=URL_NEWSAPI, params=paramNewsAPI, timeout=120)
        response.raise_for_status()
        apiData = response.json()
    except requests.exceptions.HTTPError as ex:
        print(f'\033[91m error: {ex}\033[0m')
        sys.exit()
    except requests.exceptions.ConnectionError as ex:
        print(f'\033[91m error: {ex}\033[0m')
        sys.exit()

    with open('../out/out.json', 'w', encoding="utf-8") as file:
        json.dump(apiData, file, indent=4, ensure_ascii=False)

    try:
        jsonArticles = apiData['articles']
        urlList = [url['url'] for url in jsonArticles]
    except requests.exceptions.HTTPError as ex:
        print(f'\033[91m error: {ex}\033[0m')
        sys.exit()
    except requests.exceptions.ConnectionError as ex:
        print(f'\033[91m error: {ex}\033[0m')
        sys.exit()

    tqdm.write('\nFetching...')
    articles = [fetch_Url(url) for url in tqdm(urlList, ncols=COLUMN_NUMBERS)]

    tqdm.write('\nSouping articles...')
    articlesSoup = [soup_Articles_Html(article) for article  in tqdm(articles, ncols=COLUMN_NUMBERS)]

    with open('../out/articles.json', 'w', encoding="utf-8") as file:
        json.dump(articlesSoup, file, indent=4, ensure_ascii=False)

    answerAI_json = []
    for article in articlesSoup:
        aiParam = {
            "model": OLLA_MODEL,
            "prompt": f"""Devolver o texto da notícia em primeiro lugar, mantendo todas as 
            informações originais, sem modificar nenhuma vírgula ou característica do 
            original. Não fornecer resumo, interpretação alguma, também preste atenção na 
            questão das propagandas, para retirar propagandas e a marca, 
            como VEJA, ABRIL, Olha Digital e por assim vai.
            Segue texto com o artigo: {article}""",
            "stream": False
        }

        try:
            answerAI = requests.post(url=URL_OLLAMA, json=aiParam, timeout=120)
            answerAI.raise_for_status()
            answerAI_json.append( answerAI.json())
        except requests.exceptions.HTTPError as ex:
            print(f'\033[91m error: {ex}\033[0m')
            sys.exit()
        except requests.exceptions.ConnectionError as ex:
            print(f'\033[91m error: {ex}\033[0m')
            sys.exit()
        except requests.exceptions.Timeout as ex:
            print(f'\033[91m error: {ex}\033[0m')
            sys.exit()

    with open('../out/response.json', 'w', encoding="utf-8") as file:
        json.dump(answerAI_json, file, indent=4, ensure_ascii=False)
