'''
ai search 호출 
'''

import os
from dotenv import load_dotenv ## 환경변수(.env) 정보 가져옴
from openai import AzureOpenAI

from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

import requests


load_dotenv(dotenv_path=".env", override=True) ## 환경변수 읽어옴

search_endpoint= os.getenv("SEARCH_ENDPOINT")
search_api_key = os.getenv("SEARCH_API_KEY")
openai_endpoint = os.getenv("OPENAI_ENDPOINT")
openai_api_key = os.getenv("OPENAI_API_KEY")
chat_model= os.getenv("CHAT_MODEL")

chat_client = AzureOpenAI(
    api_version = "2024-12-01-preview",
    azure_endpoint=openai_endpoint,
    api_key=openai_api_key
)

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


def azure_aisearch(index_name: str, query: str):
    client = SearchClient(
        endpoint=search_endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(search_api_key),
    )
    results = client.search(search_text=query, top=3)
    docs = [{'menu': doc['menu'], 'page': doc['page'],'desc':doc['chunk'], 'auth':doc['auth'], 'score' : doc['@search.score']} for doc in results ]#if doc['@search.score'] > 0.75]
    print(f"{index_name} , {query}")
    print(docs)

    return docs


def generate_anser(question:str, context_docs):
    try : 
        print(context_docs)
        prompt = f"""
        You are an AI assistant that answers questions **only based on the provided documents**.  
        Do not use prior knowledge or make assumptions.  
        If the answer is not clearly found in the documents, reply with:  
        **"The answer to the question is not found in the provided documents."**

        [문서]  
        {context_docs}

        [질문]  
        {question}

        [응답형식]
        메뉴경로 : {context_docs[0]['menu']}
        해당 페이지에 대한 설명

        자세한 내용은 메뉴얼 {context_docs[0]['page']}페이지를 참고하세요
        """

    # chat_client.chat.completions.create
        response = chat_client.chat.completions.create(
            model=chat_model,
            messages=[{"role": "user", "content": prompt}],
        )

        category_json = response.choices[0].message.content  # 간단 처리
        # print(category_json)
        return category_json

    except Exception as ex:
        print('Exception:')
        print(ex)
        return "The answer is not found in the documents."

