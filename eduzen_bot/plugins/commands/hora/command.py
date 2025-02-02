"""
time - time
hora - time
"""
import logging
import random

import pytz
import requests
from telegram import ChatAction

from eduzen_bot.decorators import create_user

logger = logging.getLogger()

BASE_URL = "http://worldtimeapi.org/api/timezone/"


def find_timezone(city="buenos_aires"):
    if isinstance(city, list):
        city = "_".join(city)

    for timezone in pytz.all_timezones:
        if city.replace(" ", "_").lower() in timezone.lower():
            return timezone


@create_user
def time(update, context, *args, **kwargs):
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    if not context.args:
        timezone = find_timezone()
    else:
        timezone = find_timezone(context.args)

    if not timezone:
        info = f"Mmmm... I couldn't find {timezone} but let's pick..."
        timezone = find_timezone(random.choice(pytz.all_timezones))
        update.message.reply_text(f"{info} {timezone}")

    response = requests.get(f"{BASE_URL}{timezone}")

    try:
        response.raise_for_status()
        data = response.json()
        data = data["datetime"].replace("T", "\n")
        info = f"Timezone {timezone}:\n{data}"
        update.message.reply_text(info)
    except KeyError:
        update.message.reply_text(f"No encontramos nada con '{context.args}'")
