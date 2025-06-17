"""
This code sample shows Custom Extraction Model operations with the Azure AI Document Intelligence client library.
The async versions of the samples require Python 3.8 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""

## pip install azure-ai-documentintelligence

import os
from dotenv import load_dotenv ## 환경변수(.env) 정보 가져옴
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest


load_dotenv() ## 환경변수 읽어옴

endpoint = os.getenv("DOC_INTELLIGENCE_ENDPOINT")
key = os.getenv("DOC_INTELLIGENCE_KEY")
model_id = os.getenv("CUSTOM_BUILT_MODEL_ID")

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

with open("인벤토리.pdf", "rb") as file:
    document_bytes = file.read()



# Make sure your document's type is included in the list of document types the custom model can analyze
poller = document_intelligence_client.begin_analyze_document(
    model_id, #####AnalyzeDocumentRequest(url_source=formUrl)
    body=document_bytes,     # file content or URL
    content_type="application/pdf", # document type
    pages="1-"
)
result = poller.result()

print(result.documents)
print("---")
# print(result.documents[0].bounding_regions[0])
print(result.documents[0].fields['menu']['content'])
print(result.documents[0].fields['auth']['content'])
print(result.documents[0].fields['desc']['content'])
print(result.documents[0].fields['menu']['boundingRegions'][0]['pageNumber'])

menu = "1"
desc = "2"
auth = "3"
page = "4"

## 데이터 append
data_list = []
data_list.append({"menu": menu, "desc": desc, "auth" : auth, "page" : page})



for idx, document in enumerate(result.documents):
    print(f"--------Analyzing document #{idx + 1}--------")
    for name, field in document.fields.items():
        print(f"......found field of type '{field.type}' with value '{field.content}' and with confidence {field.confidence}")


##데이터 파일로 변환

import json
# 데이터 정의
data = [{"menu": menu, "desc": desc, "auth": auth, "page": page}]

# JSON 파일로 저장
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("JSON 파일 저장 완료: data.json")

# import csv
# csv파일로 저장
with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['menu', 'desc', 'auth', 'page'])
    writer.writeheader()  # 헤더 작성
    writer.writerows(data)  # 데이터 작성

print("CSV 파일 저장 완료: data.csv")


# for idx, document in enumerate(result.documents):
#     print("--------Analyzing document #{}--------".format(idx + 1))
#     print("Document has type {}".format(document.doc_type))
#     print("Document has confidence {}".format(document.confidence))
#     print("Document was analyzed by model with ID {}".format(result.model_id))
#     for name, field in document.fields.items():
#         print("......found field of type '{}' with value '{}' and with confidence {}".format(field.type, field.content, field.confidence))


# # iterate over tables, lines, and selection marks on each page
# for page in result.pages:
#     print("\nLines found on page {}".format(page.page_number))
#     for line in page.lines:
#         print("...Line '{}'".format(line.content.encode('utf-8')))
#     for word in page.words:
#         print(
#             "...Word '{}' has a confidence of {}".format(
#                 word.content.encode('utf-8'), word.confidence
#             )
#         )
#     if page.selection_marks:
#         for selection_mark in page.selection_marks:
#             print(
#                 "...Selection mark is '{}' and has a confidence of {}".format(
#                     selection_mark.state, selection_mark.confidence
#                 )
#             )

# for i, table in enumerate(result.tables):
#     print("\nTable {} can be found on page:".format(i + 1))
#     for region in table.bounding_regions:
#         print("...{}".format(i + 1, region.page_number))
#     for cell in table.cells:
#         print(
#             "...Cell[{}][{}] has content '{}'".format(
#                 cell.row_index, cell.column_index, cell.content.encode('utf-8')
#             )
#         )
print("-----------------------------------")
