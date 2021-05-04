import datetime
import json

response = """{"centers":[{"center_id":563924,"name":"Civil Hospital 45 Plus","address":"Civil Hospital Subash Road Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Rohtak","pincode":124001,"lat":28,"long":76,"from":"09:00:00","to":"15:00:00","fee_type":"Free","sessions":[{"session_id":"76496ad0-e54f-4d19-b65e-57b85a5a93e6","date":"04-05-2021","available_capacity":0,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["09:00AM-10:00AM","10:00AM-11:00AM","11:00AM-12:00PM","12:00PM-03:00PM"]}]},{"center_id":569766,"name":"Baland PHC","address":"VPO Baland Distt Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Kalanaur","pincode":124001,"lat":28,"long":76,"from":"09:00:00","to":"18:00:00","fee_type":"Free","sessions":[{"session_id":"93269c32-1826-498c-a8d0-1bf0e648f8d3","date":"04-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["09:00AM-11:00AM","11:00AM-01:00PM","01:00PM-03:00PM","03:00PM-06:00PM"]}]},{"center_id":10907,"name":"Civil Hospital Ppc","address":"Civil Hospital Subash Road Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Rohtak","pincode":124001,"lat":28,"long":76,"from":"09:00:00","to":"15:00:00","fee_type":"Free","sessions":[{"session_id":"3db6806d-0cb3-45d3-bac5-44843bcba031","date":"04-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["09:00AM-10:00AM","10:00AM-11:00AM","11:00AM-12:00PM","12:00PM-03:00PM"]},{"session_id":"86418735-9441-4703-a304-137e419046a5","date":"04-05-2021","available_capacity":0,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["09:00AM-10:00AM","10:00AM-11:00AM","11:00AM-12:00PM","12:00PM-03:00PM"]},{"session_id":"64dce39f-b39c-4902-a8c9-4290165e4014","date":"05-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["09:00AM-10:00AM","10:00AM-11:00AM","11:00AM-12:00PM","12:00PM-03:00PM"]},{"session_id":"baec784d-8388-47ff-82e2-a9c0ef419df3","date":"06-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["09:00AM-10:00AM","10:00AM-11:00AM","11:00AM-12:00PM","12:00PM-02:30PM"]}]},{"center_id":1204,"name":"Anwal Sub Center","address":"VPO Anwal Distt.Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Kalanaur","pincode":124411,"lat":28,"long":76,"from":"09:00:00","to":"18:00:00","fee_type":"Free","sessions":[{"session_id":"28de916c-20fe-40ef-ae91-f041b27b1663","date":"04-05-2021","available_capacity":9,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["09:00AM-11:00AM","11:00AM-01:00PM","01:00PM-03:00PM","03:00PM-06:00PM"]}]},{"center_id":566387,"name":"Kharawar PHC","address":"Near Govt School VPO Kharawar District Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Sampla","pincode":124001,"lat":28,"long":76,"from":"09:00:00","to":"18:00:00","fee_type":"Free","sessions":[{"session_id":"1e2c4515-4dab-45dd-8afb-c0cd2363c875","date":"04-05-2021","available_capacity":34,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["09:00AM-11:00AM","11:00AM-01:00PM","01:00PM-03:00PM","03:00PM-06:00PM"]}]},{"center_id":629139,"name":"Hari Singh Colony Urban PHC","address":"Hari Singh Colony Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Rohtak","pincode":124001,"lat":28,"long":76,"from":"09:00:00","to":"17:00:00","fee_type":"Free","sessions":[{"session_id":"e7d5eac5-5a7f-4e87-bdfe-898359cd2789","date":"04-05-2021","available_capacity":36,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["09:00AM-11:00AM","11:00AM-01:00PM","01:00PM-03:00PM","03:00PM-05:00PM"]}]},{"center_id":570179,"name":"Banyani PHC","address":"VPO Banyani Distt Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Kalanaur","pincode":124411,"lat":28,"long":76,"from":"09:00:00","to":"16:00:00","fee_type":"Free","sessions":[{"session_id":"059c853f-fcf3-420f-b316-f47323a89612","date":"04-05-2021","available_capacity":43,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["09:00AM-11:00AM","11:00AM-01:00PM","01:00PM-03:00PM","03:00PM-04:00PM"]}]},{"center_id":693702,"name":"Sampla 18 Plus","address":"Teh Sampla","state_name":"Haryana","district_name":"Rohtak","block_name":"Sampla","pincode":124501,"lat":28,"long":76,"from":"10:00:00","to":"15:00:00","fee_type":"Free","sessions":[{"session_id":"379550f2-def0-4eab-8904-717a3b9467b5","date":"05-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["10:00AM-11:00AM","11:00AM-12:00PM","12:00PM-01:00PM","01:00PM-03:00PM"]}]},{"center_id":564532,"name":"PGIMS-Site-1-Plus18","address":"PGIMS AUDITORIUM","state_name":"Haryana","district_name":"Rohtak","block_name":"Rohtak","pincode":124001,"lat":28,"long":76,"from":"09:00:00","to":"15:00:00","fee_type":"Free","sessions":[{"session_id":"bb3ab83b-0555-4867-9a10-2f854bbad3e3","date":"05-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["09:00AM-10:00AM","10:00AM-11:00AM","11:00AM-12:00PM","12:00PM-03:00PM"]}]},{"center_id":693672,"name":"Madina 18 Plus","address":"VPO Madina Distt Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Madina","pincode":124111,"lat":28,"long":76,"from":"09:00:00","to":"13:00:00","fee_type":"Free","sessions":[{"session_id":"8b95fcce-84ad-4782-ad95-517a349c6c6c","date":"05-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["09:00AM-10:00AM","10:00AM-11:00AM","11:00AM-12:00PM","12:00PM-01:00PM"]}]},{"center_id":569356,"name":"Lakhanmajra 18 Plus","address":"Rohtak Jind Road Lakhan Majra District Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Lakhanmajra","pincode":124514,"lat":29,"long":76,"from":"09:00:00","to":"15:00:00","fee_type":"Free","sessions":[{"session_id":"b8a3de9d-df16-491b-be64-3056a0e31f63","date":"05-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["09:00AM-10:00AM","10:00AM-11:00AM","11:00AM-12:00PM","12:00PM-03:00PM"]}]},{"center_id":567481,"name":"Meham CHC","address":"Bhiwani Road Meham District Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Meham","pincode":124112,"lat":28,"long":76,"from":"09:00:00","to":"14:00:00","fee_type":"Free","sessions":[{"session_id":"35220f5f-b30d-4f58-82d3-b8d3fccce3c9","date":"05-05-2021","available_capacity":0,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["09:00AM-10:00AM","10:00AM-11:00AM","11:00AM-12:00PM","12:00PM-02:00PM"]}]},{"center_id":639116,"name":"Meham 18 Plus","address":"Meham CHC Distt Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Meham","pincode":124112,"lat":28,"long":76,"from":"09:00:00","to":"16:00:00","fee_type":"Free","sessions":[{"session_id":"69b0ee7c-5121-4cc4-87fe-3932728750c3","date":"05-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["09:00AM-11:00AM","11:00AM-01:00PM","01:00PM-03:00PM","03:00PM-04:00PM"]}]},{"center_id":693726,"name":"Chiri 18 Plus","address":"Lakhan Majra Road Chiri","state_name":"Haryana","district_name":"Rohtak","block_name":"Chiri","pincode":124514,"lat":29,"long":76,"from":"21:30:00","to":"03:30:00","fee_type":"Free","sessions":[{"session_id":"9ce3051d-5032-4c12-8178-130f23721aca","date":"05-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":[]}]},{"center_id":628701,"name":"Sukhpura Chowk UPHC","address":"Sukhpura Chowk , Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Rohtak","pincode":124001,"lat":28,"long":76,"from":"09:00:00","to":"18:00:00","fee_type":"Free","sessions":[{"session_id":"76721302-a502-45ab-a1b5-51b5f5ea6859","date":"05-05-2021","available_capacity":0,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["09:00AM-11:00AM","11:00AM-01:00PM","01:00PM-03:00PM","03:00PM-06:00PM"]}]},{"center_id":566224,"name":"Polyclinic Sector 3","address":"Polyclinic Sector 3 Rohtak","state_name":"Haryana","district_name":"Rohtak","block_name":"Rohtak","pincode":124001,"lat":28,"long":76,"from":"09:00:00","to":"18:00:00","fee_type":"Free","sessions":[{"session_id":"0fd89f48-3d9d-422b-a3e2-ed3e5312ea91","date":"05-05-2021","available_capacity":0,"min_age_limit":45,"vaccine":"COVISHIELD","slots":["09:00AM-11:00AM","11:00AM-01:00PM","01:00PM-03:00PM","03:00PM-06:00PM"]}]},{"center_id":573960,"name":"Kalanaur 18 Plus","address":"VPO Kalanaur","state_name":"Haryana","district_name":"Rohtak","block_name":"Kalanaur","pincode":124113,"lat":28,"long":76,"from":"10:00:00","to":"12:30:00","fee_type":"Free","sessions":[{"session_id":"8e98d6c3-05a0-4ebe-a935-cecbd3f56a70","date":"06-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["10:00AM-12:00PM","12:00PM-12:30PM"]},{"session_id":"8a0bb19b-fc69-4414-8262-354aa8e120cb","date":"07-05-2021","available_capacity":0,"min_age_limit":18,"vaccine":"COVISHIELD","slots":["10:00AM-12:00PM","12:00PM-12:30PM"]}]}]}"""

SESSION_FIELDS = "date", "available_capacity", "min_age_limit", "vaccine"
CENTER_FIELDS = "name", "block_name", "pincode"
default_age = 46
previous_sessions = []
count = 0


def filterDictWithFields(input_dict, fields):
    return {k: input_dict[k] for k in fields}


def formatJson(input):
    output = f"Date: {datetime.datetime.strptime(input['date'], '%d-%m-%Y').strftime('%-d %B %y')}," \
             f" Center Name: {input['name']}, City: {input['block_name']}, Pincode: {input['pincode']}" \
             f", Available Capacity: {input['available_capacity']}, Vaccine: {input['vaccine']}"
    return output


def getValidCentersWithSessionsList(centers):
    global default_age
    global previous_sessions
    current_sessions = []
    valid_centers = []
    global_valid_sessions = []
    valid_sessions = []
    for center in centers:
        filteredCenter = filterDictWithFields(center, CENTER_FIELDS)
        for session in center['sessions']:
            if session['min_age_limit'] < default_age and session['available_capacity'] > 0:
                current_sessions.append(session["session_id"])
                if session["session_id"] not in previous_sessions:
                    # print(session)
                    session = filterDictWithFields(session, SESSION_FIELDS)
                    session.update(filteredCenter)
                    valid_sessions.append(session)
    previous_sessions = current_sessions
    return valid_sessions


def getSlotsByDistrict(district_id, date):
    # print(response_json)
    response_json = json.loads(response)
    centers = response_json['centers']
    centers = getValidCentersWithSessionsList(centers)
    if len(centers) > 0:
        return centers
    else:
        return False


out = getSlotsByDistrict(1, 2)
for i in out:
    print(formatJson(i))
    print()
