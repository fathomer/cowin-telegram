from datetime import datetime


def formatDictToMessage(input_dict):
    availabilty = ""
    if input_dict['available_capacity_dose1'] > 0:
        availabilty+=f"\nDOSE 1: {input_dict['available_capacity_dose1']} Available"
    if input_dict['available_capacity_dose2'] > 0:
        availabilty+=f"\nDOSE 2: {input_dict['available_capacity_dose2']} Available"

    output = f"Date: {getFormattedDate(input_dict['date'])}\n" \
             f"Center Name: {input_dict['name']}\n" \
             f"Vaccine: {input_dict['vaccine']}" \
             f"{availabilty}\n" \
             f"<pre>Address: {input_dict['address']} - {input_dict['pincode']}</pre>"
    return output

def getFormattedDate(date):
    return datetime.strptime(date, '%d-%m-%Y').strftime('%e %B %y')

def filterDictByFields(input_dict, fields):
    return {k: input_dict[k] for k in fields}

def generateSessionKey(sessionId, date, center_id):
    return f'{sessionId}_{center_id}_{date}'