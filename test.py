import requests
import json


response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=192&date=05-05-2021")
# jsonresponse = json.loads(json.loads(response.text))
print("Response")
print("=================")
print(response.text)
