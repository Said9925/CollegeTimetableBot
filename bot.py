import os

import telebot
from telebot import types
from dotenv import load_dotenv

from html_parser import day_schedule, week_schedule

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))


Message = """
Привет! 
Данный бот позволяет смотреть расписание на день и неделю
Выберите одну из опций:
"""


Message_group = """
Введите название группы с большими буквами и без пробелов
Пример: 21-ИСП(9)-0
"""


button_day_text = "Расписание на День"
button_week_text = "Расписание на Неделю"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, Message, reply_markup=get_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == 'schedule_day')
def schedule_day(call):
    bot.send_message(call.message.chat.id, Message_group)
    bot.register_next_step_handler(call.message, process_group_day)


@bot.callback_query_handler(func=lambda call: call.data == 'schedule_week')
def schedule_week(call):
    bot.send_message(call.message.chat.id, Message_group)
    bot.register_next_step_handler(call.message, process_group_week)


def process_group_day(message):
    group_name = message.text
    bot.send_message(message.chat.id, day_schedule(group_name), reply_markup=get_keyboard())


def process_group_week(message):
    group_name = message.text
    bot.send_message(message.chat.id, week_schedule(group_name), reply_markup=get_keyboard())


def get_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_day = types.InlineKeyboardButton(text=button_day_text, callback_data='schedule_day')
    button_week = types.InlineKeyboardButton(text=button_week_text, callback_data='schedule_week')
    keyboard.add(button_day, button_week)
    return keyboard



if __name__ == "__main__":
    bot.polling(none_stop=True)