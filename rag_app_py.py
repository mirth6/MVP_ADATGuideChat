''' 기능 확인을 위한 python 코드'''

import os
from dotenv import load_dotenv ## 환경변수(.env) 정보 가져옴
from openai import AzureOpenAI
from classify_question import classify_question
from search import azure_aisearch, generate_anser


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
            "content" : """통합광고플랫폼 관련 사용자가 정보를 찾는 데 도움이 되는 AI 도우미입니다. 
            You are an AI assistant that only answers questions based on the provided documents.
            If the answer is not in the documents, say "The answer is not found in the documents."


            용어 관련 질문인 경우(index : rag-glossary),
            용어 또는 상품에 대한 설명을 제공해주세요. 문서에 기반한 내용으로 안내합니다.

            사용 관련 질문인 경우(index : rag-manual), 
            매뉴얼 문서에 기반하여 해당 기능을 사용할수 있는 메뉴경로와, 설명, 상세 내용을 확인할수 있는 매뉴얼 페이지를 안내합니다.
            인용 문서에 쓰인 메뉴경로를 그대로 답변해주세요
            [응답 형식] 
              예시) 캠페인 등록은 다음 경로에서 확인할 수 있습니다.
                    메뉴 경로 : 캠페인>캠페인등록
                    해당 페이지에 대한 설명
                    자세한 내용은 매뉴얼 {page}페이지를 참고하세요.


                """
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

        ## 질문 의도 파악해서 분기처리
        index_name = classify_question(input_text)
        # rag_manual = search_index("rag-manual",input_text)
        # rag_term = search_index("rag-term",input_text)
        ## user 입력데이터를 prompt에 추가

        prompt.append({"role":"user", "content": input_text})
        # print(prompt)

   
            
############ ai search 결과를 그대로 응답 (할루시네이션으로 인한 잘못된 답변 방지를 위해) ########
        if index_name == "rag-manual":
            context_docs = azure_aisearch(index_name,input_text)
            completion = generate_anser(input_text, context_docs)


############ RAG pattern using the AI Search index ########
        ## 아래 형태가 거의 표준     
        else :
            # index_name = "rag-glossary"
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
                            "query_type" : "vector_simple_hybrid", ## text / vector / hybrid
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
                messages=prompt,
                temperature=0.3, # 답변 다양성 줄임
                extra_body = rag_params  ##RAG 파라미터
            )

            completion = response.choices[0].message.content
            print(response.choices[0].message.context)
            # print(response.choices[0].message.context['citations'][0]['content'])




        print(completion)   



        # ## Add the response to the chat history
        # prompt.append({"role": "assistant", "content": completion})





if __name__ == "__main__" :   ## 메인실행
    main()