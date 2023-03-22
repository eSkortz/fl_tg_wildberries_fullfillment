import telebot
from telebot import types
import io
import csv
import WBApi as wb_market

bot = telebot.TeleBot('')

def changelog(message):
    markup_inline = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='🔙 Назад в главное меню', callback_data='main')
    markup_inline.add(one)
    bot.send_message(message.chat.id, f'🗂 Скоро здесь будет changelog обновлений', reply_markup=markup_inline)