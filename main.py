import requests
import json

url = "https://api.imeicheck.net/v1/account"

payload = {}
headers = {
  'Authorization': 'Bearer ',
  'Accept-Language': 'en',
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
