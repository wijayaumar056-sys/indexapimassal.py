import os
import json
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Ambil credentials dari environment variable
JSON_KEY_DATA = os.getenv('GOOGLE_CREDS')
if not JSON_KEY_DATA:
    raise ValueError("GOOGLE_CREDS tidak ditemukan di Secrets!")

# Load info credentials
info = json.loads(JSON_KEY_DATA)
credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/indexing"]
)

# Refresh credentials jika perlu
if credentials.expired:
    credentials.refresh(Request())

# Build service dengan cara yang benar
service = build('indexing', 'v3', credentials=credentials)

def index_urls():
    if not os.path.exists('urls.txt'):
        print("File urls.txt tidak ditemukan.")
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        print("urls.txt kosong.")
        return

    for url in urls:
        body = {
            'url': url,
            'type': 'URL_UPDATED'
        }
        try:
            # Eksekusi request
            response = service.urlNotifications().publish(body=body).execute()
            print(f"Sukses: {url}")
        except Exception as e:
            print(f"Gagal: {url} | Error: {e}")

if __name__ == "__main__":
    index_urls()
