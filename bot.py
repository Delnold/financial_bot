import pickle

import telebot
import requests
from dotenv import dotenv_values
from telebot.types import Message
import jsonpickle

config = dotenv_values(".env")

DJANGO_URL = config["DJANGO_URL"]
BOT_TOKEN = config["BOT_TOKEN"]

bot = telebot.TeleBot(BOT_TOKEN)


def is_command(message):
    return message.text.startswith('/')


@bot.message_handler(func=lambda message: is_command(message))
def handle_commands(message: Message):
    serialized_message = pickle.dumps(message)
    command_name = message.text
    response = requests.post(f"{DJANGO_URL}commands{command_name}", data=serialized_message)

    if response.status_code == 200:
        print(message, "Message sent to the server.")
    else:
        print(message, "Failed to send message to the server.")


@bot.message_handler(func=lambda message: not is_command(message))
def handle_message(message):
    serialized_message = pickle.dumps(message)
    response = requests.post(f"{DJANGO_URL}messages", data=serialized_message)

    if response.status_code == 200:
        print(message, "Message sent to the server.")
    else:
        print(message, "Failed to send message to the server.")


@bot.callback_query_handler(func=lambda query: True)
def handle_inline_callback(query: telebot.types.CallbackQuery):
    serialized_message = pickle.dumps(query)
    response = requests.post(f"{DJANGO_URL}callback_query", data=serialized_message)

    if response.status_code == 200:
        print(query, "Message sent to the server.")
    else:
        print(query, "Failed to send message to the server.")
