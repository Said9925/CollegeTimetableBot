import os

import telebot
from telebot import types
from dotenv import load_dotenv

from config import MESSAGE, MESSAGE_GROUP, BUTTON_DAY_TEXT, BUTTON_WEEK_TEXT
from html_parser import day_schedule, week_schedule


load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))


@bot.message_handler(commands=['start'])
def start(message):
    """
    Обрабатывает команду `/start`.
    Отправляет приветственное сообщение и клавиатуру с кнопками выбора расписания.
    """
    bot.send_message(message.chat.id, MESSAGE, reply_markup=get_keyboard())


@bot.callback_query_handler(func=lambda call: call.data == 'schedule_day')
def schedule_day(call):
    """
    Обрабатывает нажатие кнопки "Расписание на день".
    Отправляет сообщение с просьбой ввести группу и регистрирует обработчик следующего шага.
    """
    bot.send_message(call.message.chat.id, MESSAGE_GROUP)
    bot.register_next_step_handler(call.message, process_group_day)


@bot.callback_query_handler(func=lambda call: call.data == 'schedule_week')
def schedule_week(call):
    """
    Обрабатывает нажатие кнопки "Расписание на неделю".
    Отправляет сообщение с просьбой ввести группу и регистрирует обработчик следующего шага.
    """
    bot.send_message(call.message.chat.id, MESSAGE_GROUP)
    bot.register_next_step_handler(call.message, process_group_week)


def process_group_day(message):
    """
    Обрабатывает введенную группу для расписания на день.
    Отправляет расписание на день и клавиатуру с кнопками выбора расписания.
    """
    bot.send_message(message.chat.id, day_schedule(message.text), reply_markup=get_keyboard())


def process_group_week(message):
    """
    Обрабатывает введенную группу для расписания на неделю.
    Отправляет расписание на неделю и клавиатуру с кнопками выбора расписания.
    """
    bot.send_message(message.chat.id, week_schedule(message.text), reply_markup=get_keyboard())


def get_keyboard():
    """
    Создает и возвращает клавиатуру с кнопками выбора расписания.
    """
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_day = types.InlineKeyboardButton(text=BUTTON_DAY_TEXT, callback_data='schedule_day')
    button_week = types.InlineKeyboardButton(text=BUTTON_WEEK_TEXT, callback_data='schedule_week')
    keyboard.add(button_day, button_week)
    return keyboard



if __name__ == "__main__":
    bot.polling(none_stop=True)