import requests
import json
from dotenv import load_dotenv
import os



url = "https://api.imeicheck.net/v1/account"

payload = {}
headers = {
  'Authorization': f'Bearer {os.getenv("API_TOKEN")}',
  'Accept-Language': 'en',
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
