''' 통합광고플랫폼 가이드 챗봇'''

## streamlit 에서 실행 가능한 코드로 변환
## streamlit run .\01.rag-app.py  -> streamlit 실행

import os
from dotenv import load_dotenv ## 환경변수(.env) 정보 가져옴
from openai import AzureOpenAI
import streamlit as st
from classify_question import classify_question
from search import azure_aisearch, generate_anser

load_dotenv() ## 환경변수 읽어옴

openai_endpoint = os.getenv("OPENAI_ENDPOINT")
openai_api_key = os.getenv("OPENAI_API_KEY")
chat_model= os.getenv("CHAT_MODEL")
embedding_model= os.getenv("EMBEDDING_MODEL")
search_endpoint= os.getenv("SEARCH_ENDPOINT")
search_api_key = os.getenv("SEARCH_API_KEY")
index_name = os.getenv("INDEX_NAME")

#Initialize Azure OpenAI Client
chat_client = AzureOpenAI(
    api_version = "2024-12-01-preview",
    azure_endpoint=openai_endpoint,
    api_key=openai_api_key
)

st.title("GATE Assistant")
st.write("통합광고플랫폼 이용 관련 질문을 입력하세요")

## 상태를 유지하기 위해 st.session_state에 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        # 시스템 프롬프트
        {
            "role" : "system",
            "content" : """통합광고플랫폼 관련 사용자가 정보를 찾는 데 도움을 주는 AI 도우미입니다. 
You are an AI assistant that provides information specifically about the 통합광고플랫폼, which offers advertising subscription services. 
You have two responsibilities:  

1. Explain or define terms and products based on the provided documentation.  
2. Help users locate where a specific feature or function is found within the platform’s menu, including the full path.  

Rules:  
- You must answer strictly based on the provided documents.  
- If the answer is not clearly found in the documents, reply with:  
  → "The answer to this question is not found in the provided documents."  
- Do not make assumptions or generate information not present in the documents.  



                """
        },
    ]

## Display chat history
for message in st.session_state.messages : 
    if message["role"] != "system":  ## 시스템 메시지는 표시하지 않음
        st.chat_message(message["role"]).write(message["content"])




## openai 호출 함수
def get_openai_response(messages, index_name, user_input):
############ ai search 결과를 그대로 응답 (할루시네이션으로 인한 잘못된 답변 방지를 위해) ########
    if index_name == "rag-manual":
        context_docs = azure_aisearch(index_name,user_input)
        completion = generate_anser(user_input, context_docs)
        print(f"rag-manual {completion}")


############ RAG pattern using the AI Search index ########
    else :
    ## 아래 형태가 거의 표준
        rag_params = {
            "data_sources" : [
                {
                    "type":"azure_search",
                    "parameters" : {
                        "endpoint" : search_endpoint,
                        "index_name" : index_name,
                        "authentication" : {  ## 인증방법 apikey
                            "type" : "api_key",
                            "key" : search_api_key
                        },
                        "query_type" : "vector_simple_hybrid", ## text / vector / vector_simple_hybrid
                        "embedding_dependency" : { ##질문할때도 db와 동일한 모델로 임베딩되도록
                            "type" : "deployment_name",
                            "deployment_name" : embedding_model
                        },
                        "top_n_documents": 3,
                        "strictness": 3
                    },
                }
            ]
        }
   
        ## submit the chat request with RAG parameters
        response = chat_client.chat.completions.create(
            model= chat_model,
            messages=messages,
            temperature=0.3, # 답변 다양성 줄임
            extra_body = rag_params  ##RAG 파라미터
        )

        print ("respnse messages....\n",response.choices[0].message)
        completion = response.choices[0].message.content
    
    return completion




## user input
if user_input := st.chat_input("Enter your question: "):   ## :=(월러스 연산자) user_input에 값을 할당과 동시에 값 반환
    ## user 입력값 저장
    st.session_state.messages.append({"role":"user", "content": user_input})
    st.chat_message("user").write(user_input)

    ## 질문 의도 파악해서 분기처리
    index_name = classify_question(user_input)

    with st.spinner("응답을 기다리는 중..."):
         response = get_openai_response(st.session_state.messages, index_name, user_input)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

    



