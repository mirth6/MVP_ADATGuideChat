import os
from dotenv import load_dotenv ## 환경변수(.env) 정보 가져옴
from openai import AzureOpenAI

import requests


load_dotenv(dotenv_path=".env", override=True) ## 환경변수 읽어옴

search_endpoint= os.getenv("SEARCH_ENDPOINT")
search_api_key = os.getenv("SEARCH_API_KEY")

headers = {
    "Content-Type": "application/json",
    "api-key": search_api_key
}

def search_index(index_name, query):
    url = f"{search_endpoint}/indexes/{index_name}/docs/search?api-version=2024-07-01"
    print(url)
    print(query)
    payload = {
        "search": query,
        "top": 3,
        # "select": "title,menu,desc,auth,page,term,meaning" 
    }
    response = requests.post(url, headers=headers, json=payload)
    print(response.json().get("value"))
    
    return response.json()
