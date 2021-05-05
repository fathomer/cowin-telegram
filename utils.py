from datetime import datetime


def formatDictToMessage(input_dict):
    output = f"Date: {datetime.strptime(input_dict['date'], '%d-%m-%Y').strftime('%-d %B %y')}\n" \
             f"Center Name: {input_dict['name']}\nCity: {input_dict['block_name']} - {input_dict['pincode']}" \
             f"\nAvailable Capacity: {input_dict['available_capacity']}\nVaccine: {input_dict['vaccine']}"
    return output


def filterDictByFields(input_dict, fields):
    return {k: input_dict[k] for k in fields}
