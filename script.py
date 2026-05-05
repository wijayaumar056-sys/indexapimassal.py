import os
import json
import httplib2
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Ambil credentials dari environment variable (GitHub Secrets)
JSON_KEY_DATA = os.getenv('GOOGLE_CREDS')
if not JSON_KEY_DATA:
    raise ValueError("GOOGLE_CREDS tidak ditemukan di Secrets!")

info = json.loads(JSON_KEY_DATA)
credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/indexing"]
)

http = credentials.authorize(httplib2.Http())
service = build('indexing', 'v3', http=http)

def index_urls():
    if not os.path.exists('urls.txt'):
        print("File urls.txt tidak ditemukan.")
        return

    with open('urls.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        body = {
            'url': url,
            'type': 'URL_UPDATED'
        }
        try:
            response = service.urlNotifications().publish(body=body).execute()
            print(f"Sukses: {url} - {response.get('urlNotificationMetadata', {}).get('latestUpdate', {}).get('type')}")
        except Exception as e:
            print(f"Gagal: {url} | Error: {e}")

if __name__ == "__main__":
    index_urls()
