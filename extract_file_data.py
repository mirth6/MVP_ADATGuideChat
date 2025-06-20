
'''
메뉴얼(pdf) 데이터를 추출해서 json 형태로 변경
DocumentIntelligence에서 메뉴얼 형태에 맞는 custom 모델 생성
'''
## pip install azure-ai-documentintelligence

import os
from dotenv import load_dotenv ## 환경변수(.env) 정보 가져옴
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import json
import fitz  # PyMuPDF
from io import BytesIO

load_dotenv(dotenv_path=".env", override=True) ## 환경변수 읽어옴

endpoint = os.getenv("DOC_INTELLIGENCE_ENDPOINT")
key = os.getenv("DOC_INTELLIGENCE_KEY")
model_id = os.getenv("CUSTOM_BUILT_MODEL_ID")
# model_id="custom-extrc-model" 
doc_path = "통합광고플랫폼-매뉴얼.pdf"

##"YOUR_DOCUMENT"
# formUrl = "https://github.com/mirth6/ktdsTraining/blob/main/인벤토리.pdf"
#"https://khhstorage001.blob.core.windows.net/data/인벤토리.pdf"

## document_intelligence 클라이언트 생성
document_intelligence_client  = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)


# with open("1 .pdf", "rb") as file:
#     document_bytes = file.read()

doc = fitz.open(doc_path)
data_list = []

## pdf파일 한장씩 변환
for page_num in range(3,10) : ##range(len(doc)):
    single_page = fitz.open()   
    single_page.insert_pdf(doc, from_page=page_num, to_page=page_num)

    # 바이너리로 저장
    buffer = BytesIO()
    single_page.save(buffer)
    document_bytes = buffer.getvalue()


    # Make sure your document's type is included in the list of document types the custom model can analyze
    poller = document_intelligence_client.begin_analyze_document(
        model_id, #####AnalyzeDocumentRequest(url_source=formUrl)
        body=document_bytes,     # file content or URL
        content_type="application/pdf", # document type
        pages="1-"
    )
    result = poller.result()

    # print(result.documents)
    # print("---")
    # # print(result.documents[0].bounding_regions[0])
    # print(result.documents[0].fields['menu']['content'])
    # print(result.documents[0].fields['auth']['content'])
    # print(result.documents[0].fields['desc']['content'])
    # print(result.documents[0].fields['page']['content'])
    ##print(result.documents[0].fields['menu']['boundingRegions'][0]['pageNumber'])

    menu = result.documents[0].fields['menu']['content']
    desc = result.documents[0].fields['desc']['content']
    auth = result.documents[0].fields['auth']['content']
    page = result.documents[0].fields['page']['content']

    ## 데이터 append
    data_list.append({"menu": menu, "desc": desc, "auth" : auth, "page" : page})


print(f"데이터 확인... {data_list}")


# JSON 파일로 저장
with open('manual-data.json', 'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False, indent=2)

