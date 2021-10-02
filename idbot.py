#!/usr/local/bin/python3
# coding: utf-8

__author__ = "Benny <benny.think@gmail.com>"

import os
import traceback

from tqdm import tqdm
import telebot
import logging
from telebot import apihelper

from pyrogram import errors as tgerror
import logging
import os
import pathlib
import re
import tempfile
import typing
from typing import Union, Any, Iterable

from pyrogram import Client, filters, types
import math

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s [%(levelname)s]: %(message)s')

PROXY = os.getenv("PROXY")
TOKEN = os.getenv("TOKEN")
APP_ID = os.getenv("APP_ID")
APP_HASH = os.getenv("APP_HASH")


def create_app():
    _app = Client("idbot", APP_ID, APP_HASH, bot_token=TOKEN)
    if PROXY:
        _app.proxy = dict(
            hostname=PROXY.split(":")[0],
            port=int(PROXY.split(":")[1])
        )

    return _app


app = create_app()


def get_detail(user: "Union[types.User, types.Chat]") -> "str":
    if user is None:
        return "Can't get hidden forwards!"

    return f"""
user name: `@{user.username} `
first name: `{user.first_name or user.title}`
last name: `{user.last_name}`
user id: `{user.id}`

is bot: {getattr(user, "is_bot", None)}
DC: {user.dc_id}
language code: {getattr(user, "language_code", None)}
phone number: {getattr(user, "phone_number", None)}
    """


@app.on_message(filters.command(["start"]))
def start_handler(client: "Client", message: "types.Message"):
    chat_id = message.chat.id
    client.send_message(chat_id, "Welcome to Benny's ID bot.")


@app.on_message(filters.command(["help"]))
def help_handler(client: "Client", message: "types.Message"):
    chat_id = message.chat.id
    text = """Forward messages, send username, use /getme to get your account's detail.\n
    Opensource at GitHub: https://github.com/tgbot-collection/IDBot
    """
    client.send_message(chat_id, text)


@app.on_message(filters.command(["getme"]))
def getme_handler(client: "Client", message: "types.Message"):
    me = get_detail(message.from_user)
    message.reply_text(me, quote=True)


@app.on_message(filters.command(["getgroup"]))
def getgroup_handler(client: "Client", message: "types.Message"):
    me = get_detail(message.chat)
    message.reply_text(me, quote=True)


@app.on_message(filters.forwarded)
def forward_handler(client: "Client", message: "types.Message"):
    fwd = message.forward_from or message.forward_from_chat
    me = get_detail(fwd)
    message.reply_text(me, quote=True)


@app.on_message(filters.text & filters.private)
def forward_handler(client: "Client", message: "types.Message"):
    username = re.sub(r"@+|https://t.me/", "", message.text)

    try:
        user: "Union[types.User, Any]" = client.get_users(username)
        me = get_detail(user)
    except Exception as me:
        logging.error(traceback.format_exc(me))

    message.reply_text(me, quote=True)


if __name__ == '__main__':
    app.run()
