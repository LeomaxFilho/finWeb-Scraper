import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def fetchUrl(url: str) -> str:
    response = requests.Response()
    try:
        response = requests.get(url, timeout=5)
    except Exception as ex:
        tqdm.write(f'\033[91m error: {url} - exception: {ex} \033[0m')

    tqdm.write(f'\033[91m error: {url}\033[0m') if response.status_code != 200 else None

    return response.text if response.status_code == 200 else 'Error'

def soupArticlesHtml (article: str) -> str:
    soup = BeautifulSoup(article, 'html.parser')
    soupWithoutBlankLines = ''.join(soup.text.splitlines())
    
    return soupWithoutBlankLines