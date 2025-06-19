import os
from dotenv import load_dotenv ## 환경변수(.env) 정보 가져옴
from openai import AzureOpenAI
from search import search_index


def main():
    os.system('cls' if os.name == 'nt' else 'clear')  ##윈도우면 cls, 다른거면 clear
    # load_dotenv() ## 환경변수 읽어옴


    load_dotenv(dotenv_path=".env", override=True) ## 환경변수 읽어옴


    openai_endpoint = os.getenv("OPENAI_ENDPOINT")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    chat_model= os.getenv("CHAT_MODEL")
    embedding_model= os.getenv("EMBEDDING_MODEL")
    search_endpoint= os.getenv("SEARCH_ENDPOINT")
    search_api_key = os.getenv("SEARCH_API_KEY")
    index_name = os.getenv("INDEX_NAME")
    index_name2 = os.getenv("INDEX_NAME2")

    ## Initialize Azure OpenAI Client
    chat_client = AzureOpenAI(
        api_version = "2024-12-01-preview",
        azure_endpoint=openai_endpoint,
        api_key=openai_api_key
    )

    # 시스템 프롬프트 작성
    prompt = [
        {
            "role" : "system",
            "content" : "도우미에요. rag-manual을 참조하는 경우, 가져온 원본 데이터를 보여줘. rag-term을 참조하는 경우 단어의 의미를 알려줘"
        },
    ]

    while True : 
        input_text = input("Enter your question (or type 'exit' to quit): ")
        if input_text.lower() == "exit" : 
            print("Exiting the application...")
            break
        elif input_text.strip() == "": ##strip() 공백제거
            print("Please enter a valid question...")
            continue


        rag_manual = search_index("rag-manual",input_text)
        rag_term = search_index("rag-term",input_text)
        ## user 입력데이터를 prompt에 추가



        prompt.append({"role":"user", "content": input_text}).append(rag_manual).append(rag_term)
        # print(prompt)

        # ## Additional parameters to apply RAG pattern using the AI Search index
        # ## 아래 형태가 거의 표준
        # rag_params = {
        #     "data_sources" : [
        #         {
        #             "type":"azure_search",
        #             "parameters" : {
        #                 "endpoint" : search_endpoint,
        #                 "index_name" : index_name,
        #                 "authentication" : {  ## 인증방법 apikey
        #                     "type" : "api_key",
        #                     "key" : search_api_key
        #                 },
        #                 "query_type" : "vector_simple_hybrid", ## text / vector / hybrid
        #                 "embedding_dependency" : { ##질문할때도 db와 동일한 모델로 임베딩되도록
        #                     "type" : "deployment_name",
        #                     "deployment_name" : embedding_model
        #                 }
        #             },
        #         }
        #     ]
        # }


     

        ## submit the chat request with RAG parameters
        response = chat_client.chat.completions.create(
            model= chat_model,
            messages=prompt,
            # extra_body = rag_params  ##RAG 파라미터
        )
        

        completion = response.choices[0].message.content
        # print(response)
        print(completion)

        # ## Add the response to the chat history
        # prompt.append({"role": "assistant", "content": completion})




if __name__ == "__main__" :   ## 메인실행
    main()