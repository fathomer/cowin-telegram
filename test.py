import requests
import json

CALENDAR_URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}'
# response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=192&date=05-05-2021")
def getSlotsByDistrict(district_id, date):
    response = requests.get(CALENDAR_URL.format(district_id=district_id, date=date))
    return response
# jsonresponse = json.loads(json.loads(response.text))
print("Response")
print("=================")
print(getSlotsByDistrict(192,'05-05-2021').text)
