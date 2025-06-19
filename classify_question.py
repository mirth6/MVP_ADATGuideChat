'''인덱스 분기 처리를 위한 함수
사용자의 질문을 분류하여 적절한 인덱스를 선택
'''

from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# app = FastAPI()


load_dotenv(dotenv_path=".env", override=True) ## 환경변수 읽어옴


openai_endpoint = os.getenv("OPENAI_ENDPOINT")
openai_api_key = os.getenv("OPENAI_API_KEY")
chat_model= os.getenv("CHAT_MODEL")
embedding_model= os.getenv("EMBEDDING_MODEL")
search_endpoint= os.getenv("SEARCH_ENDPOINT")
search_api_key = os.getenv("SEARCH_API_KEY")
index_name = os.getenv("INDEX_NAME")


chat_client = AzureOpenAI(
    api_version = "2024-12-01-preview",
    azure_endpoint=openai_endpoint,
    api_key=openai_api_key
)

def classify_question(question):
    prompt = f"""
    당신은 사용자의 질문이 어떤 종류인지 분류하는 시스템입니다.

    다음 분류 중 하나를 선택하십시오:
    - rag-glossary-term: 질문이 용어, 정의, 개념 설명에 대한 것일 경우
    - rag-manual: 질문이 기능, 사용법, 작동 방식, 절차에 대한 것일 경우

    사용자 질문: "{question}"

    응답 형식(JSON):
    {{"category": "rag-glossary-term" 또는 "rag-manual"}}
    """
# chat_client.chat.completions.create
    response = chat_client.chat.completions.create(
        model=chat_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    category_json = eval(response.choices[0].message.content)  # 간단 처리
    print(f"인덱스 분류... {category_json['category']}")
    return category_json['category']

classify_question("인벤토리 사용현황 알고 싶어")


