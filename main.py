import logging
from datetime import datetime

import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

SESSION_FIELDS = "date", "available_capacity", "min_age_limit", "vaccine"
CENTER_FIELDS = "name", "block_name", "pincode", "sessions"
default_age = 45
previous_sessions = []
count = 0


def formatJson(input_dict):
    output = f"Date: {datetime.strptime(input_dict['date'], '%d-%m-%Y').strftime('%-d %B %y')}\n" \
             f"Center Name: {input_dict['name']}\nCity: {input_dict['block_name']} - {input_dict['pincode']}" \
             f"\nAvailable Capacity: {input_dict['available_capacity']}\nVaccine: {input_dict['vaccine']}"
    return output


def filterDictWithFields(input_dict, fields):
    return {k: input_dict[k] for k in fields}


def alarm(context: CallbackContext) -> None:
    global default_age
    global count
    global previous_sessions
    count += 1
    if count % 50 == 0:
        previous_sessions = []
    """Send the alarm message."""
    job = context.job
    print(f"Calling the api to get slots for age = {default_age}, count = {count}!")
    try:
        outputText = getSlotsByDistrict(192, datetime.today().strftime('%d-%m-%Y'))
        if outputText:
            print("Sending message")
            for center in outputText:
                context.bot.send_message(job.context, text=formatJson(center))
            context.bot.send_message(job.context, text="Login to Cowin : https://selfregistration.cowin.gov.in/")

    except Exception as e:
        logger.error(e)
        context.bot.send_message("-1001448774527", text=str(e))


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def start(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    # chat_id = update.message.chat_id
    chat_id = "-1001416312472"  # HARDCODE
    try:
        # args[0] should contain the time for the timer in seconds
        timer = 180  # TODO: Change to Constant

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(alarm, timer, context=chat_id, name=str(chat_id), first=1)

        text = 'Started successfully!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /start')


def unset(update: Update, context: CallbackContext) -> None:
    global previous_sessions
    global count
    previous_sessions = []
    count = 0
    """Remove the job if the user changed their mind."""
    # chat_id = update.message.chat_id
    chat_id = "-1001416312472"  # TODO: Constant
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def sendTelegramMessage():
    updater = Updater('')  # TODO: Secure Token
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("unset", unset))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


def getSlotsByDistrict(district_id, date):
    response = requests.get(
        'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?'
        f'district_id={district_id}&date={date}')  # TODO: Constant
    response.raise_for_status()
    response_json = response.json()
    centers = response_json['centers']
    centers = getValidCentersWithSessionsList(centers)
    if len(centers) > 0:
        return centers
    else:
        return False


def getValidCentersWithSessionsList(centers):
    global default_age
    global previous_sessions
    current_sessions = []
    valid_sessions = []
    for center in centers:
        filteredCenter = filterDictWithFields(center, CENTER_FIELDS)
        for session in center['sessions']:
            if session['min_age_limit'] < default_age and session['available_capacity'] > 0:
                current_sessions.append(session["session_id"])
                if session["session_id"] not in previous_sessions:
                    session = filterDictWithFields(session, SESSION_FIELDS)
                    session.update(filteredCenter)
                    valid_sessions.append(session)
    previous_sessions = current_sessions
    return valid_sessions


if __name__ == '__main__':
    sendTelegramMessage()
