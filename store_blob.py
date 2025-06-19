from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv ## 환경변수(.env) 정보 가져옴

load_dotenv(dotenv_path=".env", override=True) ## 환경변수 읽어옴

# def upload_blob():

# 환경 변수에서 연결 문자열 가져오기
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# 컨테이너 및 Blob 이름 설정
container_name = "manual-json"
blob_name = "manual-data.json"
file_path = "manual-data.json"

try: 

    # BlobServiceClient 생성
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # BlobClient 생성
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # 파일 업로드 및 덮어쓰기
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"Blob {blob_name} has been uploaded to container {container_name}.")

except Exception as ex:
    print('Exception:')
    print(ex)


