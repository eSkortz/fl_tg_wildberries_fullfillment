import telebot
from telebot import types
import io
import csv
import WBApi as wb_market

bot = telebot.TeleBot('')

def main(message, admins, account_name):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    one = types.InlineKeyboardButton(text='📈 Маркетплейс 📉', callback_data='Marketplace')
    two = types.InlineKeyboardButton(text='📊 Управление остатками', callback_data='Statistics')
    three = types.InlineKeyboardButton(text='💬 Отзывы', callback_data='Reviews')
    four = types.InlineKeyboardButton(text='💸 Рекламные ставки', callback_data='Advertising rates')
    five = types.InlineKeyboardButton(text='✏ Изменение параметров аккаунта', callback_data='Changing account menu')
    six = types.InlineKeyboardButton(text='⚙ Управление аккаунтами', callback_data='Account menu')
    seven = types.InlineKeyboardButton(text='👤 Добавление нового пользователя', callback_data='adm')
    eight = types.InlineKeyboardButton(text='🗂 Changelog "Trust Fullfillment"', callback_data='changelog')
    nine = types.InlineKeyboardButton(text='📖 Мануал по поключению аккаунта wb-patner', callback_data='manual')
    if account_name != 'Не выбран':
        markup_inline.add(one, two, three, four, five)
    markup_inline.add(six)
    if message.chat.id in admins:
        markup_inline.add(seven)
    markup_inline.add(eight)
    markup_inline.add(nine)
    bot.send_message(message.chat.id, f'💎💎💎 Trust Fullfilment 💎💎💎\n\nЭтот бот предназначен для работы с wb-partner, функционал бота включает:\n\n📈 Маркетплейс 📉 - управление поставками(Их составление, создание, отправка документов по поставке менеджеру на складе)\n📊 Управление остатками - редактирование количества товара на складах\n💬 Отзывы - управляйте отзывами, отвечайте на них не выходя из чата вручную или с помощью шаблонов\n💸 Рекламные ставки - просматривайте рекламные ставки для категорий, товаров, и поисковых запросов\n✏ Изменение параметров аккаунта - изменяйте уникальные идентификаторы аккаунта wb-patner и rec-id менеджера на складе\n⚙ Управление аккаунтами - бот поддерживает работу с несколькими аккаунтами wb-partner\n🗂 Changelog "Trust Fullfillment" - здесь вы сможете посмотреть информацию о последних обновлениях нашего продукта\n📖 Мануал по поключению аккаунта wb-patner - бот пришлет вам подробную инструкцию, которая поможет вам найти уникальные идентификаторы вашего аккаунта\n\n💼 Ваш текущий аккаунт "{account_name}"', reply_markup=markup_inline)