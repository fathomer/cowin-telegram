import json
import logging
from datetime import datetime
from re import S
from urllib import parse
import traceback

import requests
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext.filters import Filters
from fake_useragent import UserAgent
from telegram import Venue, Location

import config
import globals
import utils
from time import sleep


first_time=0

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    global first_time
    job = context.job
    try:
        outputText, currentidset = getSlotsByDistrict(
            config.ROHTAK_DISTRICT_ID, datetime.today().strftime('%d-%m-%Y'))
        message=''
        if outputText:
            for center in outputText:
                message+=utils.formatDictToMessage(center)+'\n\n'
            if message and not first_time:
                message+=config.DEFAULT_MESSAGE
                context.bot.send_message(
                        chat_id=job.context, text=message, parse_mode=ParseMode.HTML, timeout=20)
        globals.previous_sessions = currentidset
        first_time = 0
    except Exception as e:
        logger.exception(e)
        globals.setHeader()
        try:
            context.bot.send_message(
                        chat_id=job.context, text=message, parse_mode=ParseMode.HTML, timeout=20)
            globals.previous_sessions = currentidset
        except Exception as e:
            context.bot.send_message(config.EXCEPTION_CHANNEL_CHAT_ID, text=str(e)+"\nException from Test Code",disable_notification=True)

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

def update(update: Update, context: CallbackContext) -> None:
    chat_id = config.EXCEPTION_CHANNEL_CHAT_ID
    try:
        context.job_queue.run_once(
            updateRawResponse, 1, context=chat_id, name=str(chat_id))
        text = 'Will send next api call to update channel.'
        update.message.reply_text(text)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /start')


def sendTelegramMessage():
    updater = Updater(config.TOKEN)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler(
        "start", start, Filters.user(username="@fathomer")))
    dispatcher.add_handler(CommandHandler(
        "stop", stop, Filters.user(username="@fathomer")))
    dispatcher.add_handler(CommandHandler(
        "update", update, Filters.user(username="@fathomer")))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

def updateRawResponse(context: CallbackContext) -> None:
    """Send the raw message to test channel."""
    job = context.job
    try:
        outputText = getRawResponse(
            config.ROHTAK_DISTRICT_ID, datetime.today().strftime('%d-%m-%Y'))
        message=''
        if outputText:
            for center in outputText:
                message+=utils.formatDictToMessage(center)+'\n\n'
        context.bot.send_message(
                    job.context, text=(message))
    except Exception as e:
        logger.exception(e)
        globals.setHeader()
        context.bot.send_message(config.EXCEPTION_CHANNEL_CHAT_ID, text=str(e)+"\n FROM UPDATE COMMAND" )

def getRawResponse(district_id, date):
    response = requests.get(config.CALENDAR_URL.format(
        district_id=district_id, date=date), headers=globals.header)
    response.raise_for_status()
    centers = response.json()['centers']
    responseOut = []
    for center in centers:
        sessions = center['sessions']
        # center = utils.filterDictByFields(center, config.CENTER_FIELDS)
        for session in sessions:
            if session['min_age_limit'] <= config.MIN_AGE:
                # session = utils.filterDictByFields(
                #     session, config.SESSION_FIELDS)
                session.update(center)
                responseOut.append(session)
    return responseOut


def getSlotsByDistrict(district_id, date):
    response = requests.get(config.CALENDAR_URL.format(
        district_id=district_id, date=date), headers=globals.header)
    response.raise_for_status()
    if response.ok and response.json()['centers']:
        centers = response.json()['centers']
        return getValidCentersWithSessionsList(centers)


def getValidCentersWithSessionsList(centers):
    current_sessions_ids = dict()
    output_json_list = []
    for center in centers:
        sessions = center['sessions']
        for session in sessions:
            if session['min_age_limit'] <= config.MIN_AGE and session['available_capacity'] > 1:
                sessionKey = utils.generateSessionKey(session["session_id"],session['date'],center['center_id'])
                current_sessions_ids[sessionKey] = session['available_capacity']
                if sessionKey not in globals.previous_sessions or globals.previous_sessions[sessionKey] < session['available_capacity']:
                    session.update(center)
                    output_json_list.append(session)
                else:
                    current_sessions_ids[sessionKey] = globals.previous_sessions[sessionKey]
    # globals.previous_sessions = current_sessions_ids
    return output_json_list, current_sessions_ids


if __name__ == '__main__':
    sendTelegramMessage()
