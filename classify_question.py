# from fastapi import FastAPI, Request
from pydantic import BaseModel
# from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import os
from search import search_index
from dotenv import load_dotenv

# app = FastAPI()


load_dotenv(dotenv_path=".env", override=True) ## 환경변수 읽어옴

# Azure 설정
AZURE_OPENAI_DEPLOYMENT = os.getenv("CHAT_MODEL") # 모델 이름
AZURE_OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("OPENAI_KEY")

SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("SEARCH_API_KEY")
INDEX_MAP = {
    "glossary": "glossary-index",
    "manual": "manual-index"
}

# OpenAI 설정

# openai.api_type = "azure"
# openai.api_base = AZURE_OPENAI_ENDPOINT
# openai.api_key = AZURE_OPENAI_KEY
# openai.api_version = "2023-12-01"

chat_client = AzureOpenAI(
    api_version = "2024-12-01-preview",
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY
)

# class QuestionInput(BaseModel):
#     question: str

def classify_question(question):
    prompt = f"""
당신은 사용자의 질문이 어떤 종류인지 분류하는 시스템입니다.

다음 분류 중 하나를 선택하십시오:
- glossary: 질문이 용어, 정의, 개념 설명에 대한 것일 경우
- manual: 질문이 기능, 사용법, 작동 방식, 절차에 대한 것일 경우

사용자 질문: "{question}"

응답 형식(JSON):
{{"category": "glossary" 또는 "manual"}}
    """
# chat_client.chat.completions.create
    response = chat_client.chat.completions.create(
        engine=AZURE_OPENAI_DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    category_json = eval(response['choices'][0]['message']['content'])  # 간단 처리
    print(category_json['category'])
    return category_json['category']

classify_question("큐톤이뭐야?")

# def search_azure_ai(index_name: str, query: str):
#     client = SearchClient(
#         endpoint=SEARCH_ENDPOINT,
#         index_name=index_name,
#         credential=AzureKeyCredential(SEARCH_KEY),
#     )
#     results = client.search(search_text=query, top=3)
#     docs = [doc['content'] for doc in results]
#     return docs

# @app.post("/ask")
# async def ask_question(data: QuestionInput):
#     category = classify_question(data.question)
#     index_name = INDEX_MAP[category]
#     search_results = search_azure_ai(index_name, data.question)

#     return {
#         "category": category,
#         "index_used": index_name,
#         "top_matches": search_results
#     }
