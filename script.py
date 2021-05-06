import logging
from datetime import datetime

import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext.filters import Filters
from fake_useragent import UserAgent

import config
import globals
import utils

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    try:
        outputText = getSlotsByDistrict(
            192, datetime.today().strftime('%d-%m-%Y'))
        if outputText:
            for center in outputText:
                context.bot.send_message(
                    job.context, text=utils.formatDictToMessage(center))
            context.bot.send_message(job.context, text=config.DEFAULT_MESSAGE)

    except Exception as e:
        logger.error(e)
        globals.setHeader()
        context.bot.send_message(config.EXCEPTION_CHANNEL_CHAT_ID, text=str(e))


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def start(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue for one chat."""
    chat_id = config.ROHTAK_CHANNEL_CHAT_ID
    try:
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(
            alarm, config.POLLING_INTERVAL, context=chat_id, name=str(chat_id), first=1)
        text = 'Started bot successfully.'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /start')


def stop(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = config.ROHTAK_CHANNEL_CHAT_ID
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Bot successfully stopped' if job_removed else 'Bot is not running.'
    update.message.reply_text(text)


def sendTelegramMessage():
    updater = Updater(config.TOKEN)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler(
        "start", start, Filters.user(username="@fathomer")))
    dispatcher.add_handler(CommandHandler(
        "stop", stop, Filters.user(username="@fathomer")))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


def getSlotsByDistrict(district_id, date):
    ua = UserAgent()
    header = {'User-Agent': str(ua.random)} 
    response = requests.get(config.CALENDAR_URL.format(
        district_id=district_id, date=date), headers=header)
    response.raise_for_status()
    centers = response.json()['centers']
    return getValidCentersWithSessionsList(centers)


def getValidCentersWithSessionsList(centers):
    current_sessions_ids = []
    output_json_list = []
    for center in centers:
        sessions = center['sessions']
        center = utils.filterDictByFields(center, config.CENTER_FIELDS)
        for session in sessions:
            if session['min_age_limit'] <= config.MIN_AGE and session['available_capacity'] > 0:
                current_sessions_ids.append(session["session_id"])
                if session["session_id"] not in globals.previous_sessions:
                    session = utils.filterDictByFields(
                        session, config.SESSION_FIELDS)
                    session.update(center)
                    output_json_list.append(session)
    globals.previous_sessions = current_sessions_ids
    globals.count += 1
    return output_json_list


if __name__ == '__main__':
    sendTelegramMessage()
