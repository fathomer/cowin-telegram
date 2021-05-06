import requests
from fake_useragent import UserAgent
ua = UserAgent()

CALENDAR_URL = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}'
# response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=192&date=05-05-2021")


def getSlotsByDistrict(district_id, date):
    header = {'User-Agent': str(ua.random)}
    response = requests.get(CALENDAR_URL.format(
        district_id=district_id, date=date), headers=header)
    return response


# jsonresponse = json.loads(json.loads(response.text))
print("Response")
print("=================")
print(getSlotsByDistrict(192, '05-05-2021').text)
