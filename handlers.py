import os

from dotenv import load_dotenv
import telebot


from config import MESSAGE, MESSAGE_GROUP
from html_parser import day_schedule, week_schedule
from utils import get_keyboard


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