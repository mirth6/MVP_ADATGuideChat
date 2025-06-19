
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

print(endpoint)
print(key)
print(model_id)

model_id="custom-extrc-model" 

##"YOUR_DOCUMENT"
# formUrl = "https://github.com/mirth6/ktdsTraining/blob/main/인벤토리.pdf"
#"https://khhstorage001.blob.core.windows.net/data/인벤토리.pdf"


# Azure 포털에 로그인합니다.
# 스토리지 계정으로 이동합니다.
# 설정 섹션에서 구성을 선택합니다.
# 공용 Blob 액세스 설정을 확인하고, 필요에 따라 변경합니다

document_intelligence_client  = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

print(os.getcwd())

# document_bytes = split_pdf_with_pymupdf("인벤토리.pdf",".",0)

# with open("1 .pdf", "rb") as file:
#     document_bytes = file.read()

doc = fitz.open("통합광고플랫폼-사용자매뉴얼(영업사).pdf")
data_list = []

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

    print(result.documents)
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


print(data_list)


# JSON 파일로 저장
with open('manual-data.json', 'w', encoding='utf-8') as f:
    json.dump(data_list, f, ensure_ascii=False, indent=2)

