import telebot
from telebot import types
import io
import csv
import WBApi as wb_market

bot = telebot.TeleBot('')

def change_account(message, wb_accounts):
    markup_inline = types.InlineKeyboardMarkup()
    markup_list = []
    for i in range(1, len(wb_accounts)):
        if message.chat.id in wb_accounts[i]['auth']:
            markup_list.append(types.InlineKeyboardButton(text=f'💼 {wb_accounts[i]["name"]}',
                                                          callback_data=f'Changing account|{wb_accounts[i]["name"]}'))
    for i in range(len(markup_list)):
        markup_inline.add(markup_list[i])
    one = types.InlineKeyboardButton(text='🔙 Назад в главное меню', callback_data='main')
    markup_inline.add(one)
    bot.send_message(message.chat.id, f'💼 Список аккаунтов:', reply_markup=markup_inline)

def changing_account(message, id):
    markup_inline = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='🔙 Назад в главное меню', callback_data='main')
    markup_inline.add(one)
    bot.send_message(message.chat.id, f'✅ Аккаунт успешно изменен на {id}', reply_markup=markup_inline)

def delete_account(message, wb_accounts):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    markup_list = []
    for i in range(1, len(wb_accounts)):
        if message.chat.id in wb_accounts[i]['auth']:
            markup_list.append(types.InlineKeyboardButton(text=f'🗑 {wb_accounts[i]["name"]}',
                                                          callback_data=f'Deliting account|{wb_accounts[i]["name"]}'))
    for i in range(len(markup_list)):
        markup_inline.add(markup_list[i])
    four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
    markup_inline.add(four)
    bot.send_message(message.chat.id, 'Выберите аккаунт, который хотите удалить 🗑', reply_markup=markup_inline)

def deliting_account(message, name):
    AddList = []
    with io.open('wb_accounts.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != name:
                AddList.append(row)
    with io.open('wb_accounts.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    AddList = []
    with io.open('reviews_sample.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != name:
                AddList.append(row)
    with io.open('reviews_sample.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    AddList = []
    with io.open('users_session.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if int(row[0]) != message.chat.id:
                AddList.append(row)
            else:
                string = []
                string.append(message.chat.id)
                string.append('Не выбран')
                for i in range(0,5):
                    string.append(0)
                AddList.append(string)
    with io.open('users_session.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    markup_inline = types.InlineKeyboardMarkup()
    four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
    markup_inline.add(four)
    bot.send_message(message.chat.id, f'✅ Аккаунт {name} успешно удален', reply_markup=markup_inline)

def change_wb_api(message, ApiToken):
    markup_inline = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='⚙ Изменить API-key', callback_data='Change API-key')
    two = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
    markup_inline.add(one, two)
    bot.send_message(message.chat.id, f'Ваш API-token: {ApiToken}', reply_markup=markup_inline)

def change_rec_id(message, RecipientId):
    markup_inline = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='⚙ Изменить rec-id', callback_data='Changing rec-id')
    two = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
    markup_inline.add(one, two)
    bot.send_message(message.chat.id, f'Ваш recipient-id: {RecipientId}', reply_markup=markup_inline)

def change_wb_token(message, WBToken):
    markup_inline = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='⚙ Изменить WBToken', callback_data='Change WBT')
    two = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
    markup_inline.add(one, two)
    bot.send_message(message.chat.id, f'Ваш WBToken: {WBToken}', reply_markup=markup_inline)

def change_sup_id(message, x_supplier_id):
    markup_inline = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='⚙ Изменить x_supplier_id', callback_data='Change x_sup')
    two = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
    markup_inline.add(one, two)
    bot.send_message(message.chat.id, f'Ваш x_supplier_id: {x_supplier_id}', reply_markup=markup_inline)