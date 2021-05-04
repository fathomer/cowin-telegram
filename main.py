import requests
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime

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


def filterDictWithFields(input_dict, fields):
    return {k: input_dict[k] for k in fields}


def countUnit(n):
    return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')


def alarm(context: CallbackContext) -> None:
    global default_age
    global count
    global previous_sessions
    count += 1
    if count % 10 == 0:
        previous_sessions = []
    """Send the alarm message."""
    job = context.job
    print(f"Calling the api to get slots for age = {default_age}, count = {count}!")
    try:
        outputText = getSlotsByDistrict(192, datetime.today().strftime('%d-%m-%Y'))
    except Exception as e:
        loggger.error(e)
        outputText = str(e)
    if outputText:
        print("Sending message")
        context.bot.send_message(job.context, text=outputText)


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return
        elif due < 5:
            update.message.reply_text('Sorry minimum 5 seconds is required.!')
            return
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(alarm, due, context=chat_id, name=str(chat_id), first=0)

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(update: Update, context: CallbackContext) -> None:
    global previous_sessions
    global count
    previous_sessions = []
    count = 0
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def sendTelegramMessage():
    updater = Updater('1649699075:AAE34izKebh1QmOhv6pt4deD9o-ysfqM2v4')
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_timer))
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
        f'district_id={district_id}&date={date}')
    response.raise_for_status()
    response_json = response.json()
    # print(response_json)
    centers = response_json['centers']
    centers = getValidCentersWithSessionsList(centers)
    if len(centers) > 0:
        return str(centers)
    else:
        return False


def getValidCentersWithSessionsList(centers):
    global default_age
    global previous_sessions
    current_sessions = []
    valid_centers = []
    for center in centers:
        valid_sessions = []
        for session in center['sessions']:
            if session['min_age_limit'] < default_age and session['available_capacity'] > 0:
                current_sessions.append(session["session_id"])
                if session["session_id"] not in previous_sessions:
                    # print(session)
                    session = filterDictWithFields(session, SESSION_FIELDS)
                    valid_sessions.append(session)
        if len(valid_sessions) > 0:
            center['sessions'] = valid_sessions
            center = filterDictWithFields(center, CENTER_FIELDS)
            valid_centers.append(center)
    previous_sessions = current_sessions
    return valid_centers


if __name__ == '__main__':
    sendTelegramMessage()
