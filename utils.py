from telebot import types

from config import BUTTON_DAY_TEXT, BUTTON_WEEK_TEXT

def get_keyboard():
    """
    Создает и возвращает клавиатуру с кнопками выбора расписания.
    """
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button_day = types.InlineKeyboardButton(text=BUTTON_DAY_TEXT, callback_data='schedule_day')
    button_week = types.InlineKeyboardButton(text=BUTTON_WEEK_TEXT, callback_data='schedule_week')
    keyboard.add(button_day, button_week)
    return keyboard