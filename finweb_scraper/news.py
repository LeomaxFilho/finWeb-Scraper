import os, json, requests, sys
from tqdm import tqdm
from dotenv import load_dotenv
from utils import fetchUrl, soupArticlesHtml

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
        response = requests.get(url=URL_NEWSAPI, params=paramNewsAPI)
        response.raise_for_status()
        apiData = response.json()
    except Exception as ex:
        print(f'\033[91m error: {ex}\033[0m')
        sys.exit()
    
    with open('out/out.json', 'w') as file:
        json.dump(apiData, file, indent=4, ensure_ascii=False)

    try:
        jsonArticles = apiData['articles']
        urlList = [url['url'] for url in jsonArticles]
    except Exception as ex:
        print(f'\033[91m error: {ex}\033[0m')
    
    tqdm.write('\nFetching...')
    articles = [fetchUrl(url) for url in tqdm(urlList, ncols=COLUMN_NUMBERS)]
    
    tqdm.write('\nSouping articles...')
    articlesSoup = [soupArticlesHtml(article) for article  in tqdm(articles, ncols=COLUMN_NUMBERS)]

    with open('out/articles.json', 'w') as file:
        json.dump(articlesSoup, file, indent=4, ensure_ascii=False)
    
    answerAI_json = []
    for article in articlesSoup:
        aiParam = {
            "model": OLLA_MODEL,
            "prompt": f"""Devolver o texto da notícia em primeiro lugar, mantendo todas as informações originais, sem modificar nenhuma vírgula, pontuação ou característica do original. Não fornecer resumo, análise ou interpretação alguma, também preste atenção na questão das propagandas, para retirar propagandas e a marca, como VEJA, ABRIL, Olha Digital e por assim vai.
                Segue texto com o artigo: {article}""",
            "stream": False
        }
        
        try:
            answerAI = requests.post(url=URL_OLLAMA, json=aiParam)
            answerAI.raise_for_status()
            answerAI_json.append( answerAI.json())
        except Exception as ex:
            print(f'\033[91m error in AI API request: {ex}\033[0m')
            continue
    
    with open('out/response.json', 'w') as file:
        json.dump(answerAI_json, file, indent=4, ensure_ascii=False)
