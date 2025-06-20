# 통합광고플랫폼 가이드 챗봇
url : khh-webapp.azurewebsites.net

설명 : 통합광고플랫폼 
1. 통합광고플랫폼 상품 및 광고 용어등에 대해 설명해줍니다.
2. 통합광고플랫폼 기능이 어느 메뉴에 위치해 있는지 알려주고, 간략한 설명과 함께 매뉴얼 위치를 제공합니다.

##코드
[챗봇]
app.py 
classify-question.py
search.py 

[데이터 전처리]
extract_file_data.py
store_blob.py


설정 > 구성 > 시작명령
bash /home/site/wwwroot/streamlit.sh
로그스트림에서 에러 확인



Azure 포털에서 Azure Search 서비스로 이동
설정 > "시맨틱 검색"으로 이동



# Resource Group의 생성
echo "Resource Group creating..."
az group create --name khh-rg --location eastus

# OpenAI Service 생성
echo "OpenAI Service creating..."
az cognitiveservices account create --name khh-openai-0619 --resource-group khh-rg --kind OpenAI --sku S0 --location eastus

# Azure AI Search의 생성
echo "Azure AI Search creating..."
az search service create --name khh-search-0619 --resource-group khh-rg --sku Basic --partition-count 1 --replica-count 1

# Azure Storage Accout의 생성
echo "Azure Storage Account creating..."
az storage account create --name khhstorage0619 --resource-group khh-rg --location eastus --sku Standard_LRS

# 컨테이너 생성
echo "Blob storage container creating in Azure Storage Account"
az storage container create --name pdf-data --account-name khhstorage0619
