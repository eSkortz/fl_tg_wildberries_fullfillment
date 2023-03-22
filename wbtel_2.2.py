import telebot
from telebot import types
import io
import csv
import WBClient as wb_client
import Callback_main as wb_main
import Callback_marketplace as wb_marketplace
import Callback_statistics as wb_statistics
import Callback_reviews as wb_reviews
import Callback_accounts as wb_account
import Callback_changelog as wb_changelog

bot = telebot.TeleBot('')

bot_users = []
wb_accounts = []
account_reviews = []
users_session = []
admins = [588339594, 377372793]

create_account = []

def init():
    global bot_users
    global wb_accounts
    global account_reviews
    bot_users = []
    with io.open('bot_users.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            bot_users.append(int(row[0]))
    wb_accounts = []
    with io.open('wb_accounts.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            account = {
                'name': row[0],
                'ApiToken': row[1],
                'RecipientId': row[2],
                'WBToken': row[3],
                'x_supplier_id': row[4],
                'auth': row[5].split(';')
            }
            for i in range(len(account['auth'])):
                account['auth'][i] = int(account['auth'][i])
            wb_accounts.append(account)
    account_reviews = []
    with io.open('reviews_sample.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            account = {
                'name': row[0],
                'first': row[1],
                'second': row[2],
                'third': row[3],
                'fourth': row[4],
                'fifth': row[5]
            }
            account_reviews.append(account)
init()

def init_session():
    global users_session
    users_session = []
    with io.open('users_session.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            session = {
                'id' : row[0],
                'name' : row[1],
                'pointer_create' : row[2],
                'name_create' : row[3],
                'pointer_stocks' : row[4],
                'stock' : row[5],
                'pointer_create_sample' : row[6]
            }
            users_session.append(session)
init_session()

#Изменение recipient-id
def RefererChoice1(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            session_name = users_session[i]['name']
    for i in range(len(wb_accounts)):
        if wb_accounts[i]['name'] == session_name:
            account_name = wb_accounts[i]['name']
    newRecipientId = message.text
    AddList = []
    with io.open('wb_accounts.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != account_name:
                AddList.append(row)
            else:
                string = []
                string.append(row[0])
                string.append(row[1])
                string.append(newRecipientId)
                string.append(row[3])
                string.append(row[4])
                string.append(row[5])
                AddList.append(string)
    with io.open('wb_accounts.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    init()
    choice(message)
#Изменение WBAPI-токена
def WbbApi(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            session_name = users_session[i]['name']
    for i in range(len(wb_accounts)):
        if wb_accounts[i]['name'] == session_name:
            account_name = wb_accounts[i]['name']
    newApiToken = message.text
    AddList = []
    with io.open('wb_accounts.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != account_name:
                AddList.append(row)
            else:
                string = []
                string.append(row[0])
                string.append(newApiToken)
                string.append(row[2])
                string.append(row[3])
                string.append(row[4])
                string.append(row[5])
                AddList.append(string)
    with io.open('wb_accounts.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    init()
    choice(message)
#Изменение WBToken
def WbbWBT(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            session_name = users_session[i]['name']
    for i in range(len(wb_accounts)):
        if wb_accounts[i]['name'] == session_name:
            account_name = wb_accounts[i]['name']
    newWBToken = message.text
    AddList = []
    with io.open('wb_accounts.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != account_name:
                AddList.append(row)
            else:
                string = []
                string.append(row[0])
                string.append(row[1])
                string.append(row[2])
                string.append(newWBToken)
                string.append(row[4])
                string.append(row[5])
                AddList.append(string)
    with io.open('wb_accounts.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    init()
    choice(message)
#Изменение x_supplier_id
def WbbXSP(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            session_name = users_session[i]['name']
    for i in range(len(wb_accounts)):
        if wb_accounts[i]['name'] == session_name:
            account_name = wb_accounts[i]['name']
    newx_supplier_id = message.text
    AddList = []
    with io.open('wb_accounts.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != account_name:
                AddList.append(row)
            else:
                string = []
                string.append(row[0])
                string.append(row[1])
                string.append(row[2])
                string.append(row[3])
                string.append(newx_supplier_id)
                string.append(row[5])
                AddList.append(string)
    with io.open('wb_accounts.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    init()
    choice(message)
#Ответ на отзыв
def reply_to_review(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            users_session[i]['name_create'] = message.text
            users_session[i]['pointer_create'] = 1
#Поиск рекламных ставок по ключевому слову
def advertising_by_keyword(message):
    keyword = message.text
    jsn = wb_client.GetByKeyword(keyword)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        try:
            CpmList = []
            for i in range(len(jsn['adverts'])):
                CpmList.append(int(jsn['adverts'][i]['cpm']))
            markup_inline = types.InlineKeyboardMarkup()
            markup_list = []
            for i in range(len(CpmList)):
                markup_list.append(types.InlineKeyboardButton(text=f'{i+1} : {CpmList[i]}', callback_data='none'))
            if len(markup_list) >= 10:
                for i in range(0, 10):
                    markup_inline.add(markup_list[i])
            else:
                for i in range(len(markup_list)):
                    markup_inline.add(markup_list[i])
            four = types.InlineKeyboardButton(text='🔙 Вернуться в меню рекламных ставок', callback_data='Advertising rates')
            markup_inline.add(four)
            bot.send_message(message.chat.id, f'🗝 Рекламные ставки по заданному ключевому слову ({keyword})', reply_markup=markup_inline)
        except Exception:
            markup_inline = types.InlineKeyboardMarkup()
            four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
            markup_inline.add(four)
            bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
# Поиск рекламных ставок по ключевому слову
def advertising_by_good(message):
    url = message.text
    jsn = wb_client.GetByGood(url)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        try:
            CpmList = []
            for i in range(len(jsn)):
                CpmList.append(int(jsn[i]['cpm']))
            markup_inline = types.InlineKeyboardMarkup()
            markup_list = []
            for i in range(len(CpmList)):
                markup_list.append(types.InlineKeyboardButton(text=f'{i + 1} : {CpmList[i]}', callback_data='none'))
            if len(markup_list) >= 10:
                for i in range(0, 10):
                    markup_inline.add(markup_list[i])
            else:
                for i in range(len(markup_list)):
                    markup_inline.add(markup_list[i])
            four = types.InlineKeyboardButton(text='🔙 Вернуться в меню рекламных ставок', callback_data='Advertising rates')
            markup_inline.add(four)
            bot.send_message(message.chat.id, f'🧸 Рекламные ставки по заданному товару ({url})', reply_markup=markup_inline)
        except Exception:
            markup_inline = types.InlineKeyboardMarkup()
            four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
            markup_inline.add(four)
            bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
# Поиск рекламных ставок по ключевому слову
def advertising_by_category(message):
    url = message.text
    jsn = wb_client.GetByCategory(url)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        try:
            CpmList = []
            for i in range(len(jsn['adverts'])):
                CpmList.append(int(jsn['adverts'][i]['cpm']))
            markup_inline = types.InlineKeyboardMarkup()
            markup_list = []
            for i in range(len(CpmList)):
                markup_list.append(types.InlineKeyboardButton(text=f'{i + 1} : {CpmList[i]}', callback_data='none'))
            if len(markup_list) >= 10:
                for i in range(0, 10):
                    markup_inline.add(markup_list[i])
            else:
                for i in range(len(markup_list)):
                    markup_inline.add(markup_list[i])
            four = types.InlineKeyboardButton(text='🔙 Вернуться в меню рекламных ставок', callback_data='Advertising rates')
            markup_inline.add(four)
            bot.send_message(message.chat.id, f'🛍 Рекламные ставки по заданной категории ({url})', reply_markup=markup_inline)
        except Exception:
            markup_inline = types.InlineKeyboardMarkup()
            four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
            markup_inline.add(four)
            bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)

#Создание новой поставки
def CreateSupply(message):
    msg = bot.send_message(message.chat.id, 'Введите название поставки: ')
    bot.register_next_step_handler(msg, CreateSup)
def CreateSup(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            users_session[i]['name_create'] = message.text
            users_session[i]['pointer_create'] = 1

#Изменение кол-ва товара на складе
def ChangeStocks(message):
    msg = bot.send_message(message.chat.id, 'Введите кол-во товара: ')
    bot.register_next_step_handler(msg, ChangeSto)
def ChangeSto(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            users_session[i]['stock'] = message.text
            users_session[i]['pointer_stocks'] = 1

def change_account(id, name):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == id:
            users_session[i]['name'] = name
    with io.open('users_session.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(users_session)):
            AddList = []
            AddList.append(users_session[i]['id'])
            AddList.append(users_session[i]['name'])
            AddList.append(users_session[i]['pointer_create'])
            AddList.append(users_session[i]['name_create'])
            AddList.append(users_session[i]['pointer_stocks'])
            AddList.append(users_session[i]['stock'])
            AddList.append(users_session[i]['pointer_create_sample'])
            writer.writerow(AddList)

def create_account_1(message):
    msg = bot.send_message(message.chat.id, 'Введите имя аккаунта: ')
    bot.register_next_step_handler(msg, create_account_2)
def create_account_2(message):
    global create_account
    create_account = []
    create_account.append(message.text)
    msg = bot.send_message(message.chat.id, 'Введите WB Api Token: ')
    bot.register_next_step_handler(msg, create_account_3)
def create_account_3(message):
    global create_account
    create_account.append(message.text)
    msg = bot.send_message(message.chat.id, 'Введите Recipient-id: ')
    bot.register_next_step_handler(msg, create_account_4)
def create_account_4(message):
    global create_account
    create_account.append(message.text)
    msg = bot.send_message(message.chat.id, 'Введите WBToken: ')
    bot.register_next_step_handler(msg, create_account_5)
def create_account_5(message):
    global create_account
    create_account.append(message.text)
    msg = bot.send_message(message.chat.id, 'Введите x-supplier-id: ')
    bot.register_next_step_handler(msg, write_creating_account_to_file)
def write_creating_account_to_file(message):
    name = create_account[0]
    create_account.append(message.text)
    create_account.append(message.chat.id)
    with io.open('wb_accounts.csv', mode= 'a', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = '|', lineterminator="\n")
        file_writer.writerow(create_account)
    with io.open('reviews_sample.csv', mode= 'a', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter='|', lineterminator="\n")
        account_review = []
        account_review.append(create_account[0])
        account_review.append('Здесь должен быть шаблон ответа для отзыва 1/5')
        account_review.append('Здесь должен быть шаблон ответа для отзыва 2/5')
        account_review.append('Здесь должен быть шаблон ответа для отзыва 3/5')
        account_review.append('Здесь должен быть шаблон ответа для отзыва 4/5')
        account_review.append('Здесь должен быть шаблон ответа для отзыва 5/5')
        file_writer.writerow(account_review)
    init()
    markup_inline = types.InlineKeyboardMarkup()
    four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
    markup_inline.add(four)
    bot.send_message(message.chat.id, f'✅ Аккаунт {name} успешно создан', reply_markup=markup_inline)

def adm_1(message):
    if message.chat.id in admins:
        msg = bot.send_message(message.chat.id, 'Введите нового пользователя: ')
        bot.register_next_step_handler(msg, adm_2)
    else:
        bot.send_message(message.chat.id, f'🤗 Извините, кажется у вас нет доступа к админ панели')
def adm_2(message):
    new_account_id = []
    new_account_id.append(message.text)
    with io.open('bot_users.csv', mode= 'a', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = '|', lineterminator="\n")
        file_writer.writerow(new_account_id)
    init()
    with io.open('users_session.csv', mode= 'a', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = '|', lineterminator="\n")
        string = []
        string.append(message.text)
        string.append('Не выбран')
        for i in range(0,5):
            string.append(0)
        file_writer.writerow(string)
    markup_inline = types.InlineKeyboardMarkup()
    four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
    markup_inline.add(four)
    bot.send_message(message.chat.id, f'✅ Аккаунт {message.text} успешно создан', reply_markup=markup_inline)

def sample_change_1(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            name = users_session[i]['name']
    new_sample = message.text
    AddList = []
    with io.open('reviews_sample.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != name:
                AddList.append(row)
            else:
                string = []
                string.append(row[0])
                string.append(new_sample)
                string.append(row[2])
                string.append(row[3])
                string.append(row[4])
                string.append(row[5])
                AddList.append(string)
    with io.open('reviews_sample.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            users_session[i]['pointer_create_sample'] = 1
def sample_change_2(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            name = users_session[i]['name']
    new_sample = message.text
    AddList = []
    with io.open('reviews_sample.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != name:
                AddList.append(row)
            else:
                string = []
                string.append(row[0])
                string.append(row[1])
                string.append(new_sample)
                string.append(row[3])
                string.append(row[4])
                string.append(row[5])
                AddList.append(string)
    with io.open('reviews_sample.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            users_session[i]['pointer_create_sample'] = 1
def sample_change_3(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            name = users_session[i]['name']
    new_sample = message.text
    AddList = []
    with io.open('reviews_sample.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != name:
                AddList.append(row)
            else:
                string = []
                string.append(row[0])
                string.append(row[1])
                string.append(row[2])
                string.append(new_sample)
                string.append(row[4])
                string.append(row[5])
                AddList.append(string)
    with io.open('reviews_sample.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            users_session[i]['pointer_create_sample'] = 1
def sample_change_4(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            name = users_session[i]['name']
    new_sample = message.text
    AddList = []
    with io.open('reviews_sample.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != name:
                AddList.append(row)
            else:
                string = []
                string.append(row[0])
                string.append(row[1])
                string.append(row[2])
                string.append(row[3])
                string.append(new_sample)
                string.append(row[5])
                AddList.append(string)
    with io.open('reviews_sample.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            users_session[i]['pointer_create_sample'] = 1
def sample_change_5(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            name = users_session[i]['name']
    new_sample = message.text
    AddList = []
    with io.open('reviews_sample.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != name:
                AddList.append(row)
            else:
                string = []
                string.append(row[0])
                string.append(row[1])
                string.append(row[2])
                string.append(row[3])
                string.append(row[4])
                string.append(new_sample)
                AddList.append(string)
    with io.open('reviews_sample.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            users_session[i]['pointer_create_sample'] = 1

@bot.message_handler(commands=['recipient'])
def main(message):
    bot.send_message(message.chat.id, f'Ваш recipient-id: {message.chat.id}')

@bot.message_handler(content_types=['text','audio','document','photo'])
@bot.message_handler(commands=['start'])
def choice(message):
    init()
    init_session()
    if message.chat.id in bot_users:
        for i in range(len(users_session)):
            if int(users_session[i]['id']) == message.chat.id:
                session_name = users_session[i]['name']
        for i in range(len(wb_accounts)):
            if wb_accounts[i]['name'] == session_name:
                account_name = wb_accounts[i]['name']
        wb_main.main(message, admins, account_name)
    else:
        bot.send_message(message.chat.id, '🤗 Извините, кажется у вас нет доступа к боту, получите ваш id с помощью /recipient и попросите администратора проекта добавить вас в список пользователей')

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    init()
    init_session()
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == call.message.chat.id:
            session_name = users_session[i]['name']
    for i in range(len(wb_accounts)):
        if wb_accounts[i]['name'] == session_name:
            account_name = wb_accounts[i]['name']
            ApiToken = wb_accounts[i]['ApiToken']
            RecipientId = wb_accounts[i]['RecipientId']
            WBToken = wb_accounts[i]['WBToken']
            x_supplier_id = wb_accounts[i]['x_supplier_id']

    calling_data = call.data.split('|')

    if calling_data[0] == 'main':
        wb_main.main(call.message, admins, account_name)

    if calling_data[0] == 'Marketplace':
        wb_marketplace.marketplace(call.message, WBToken, x_supplier_id)
    if calling_data[0] == 'List of new orders':
        next = calling_data[1]
        count = calling_data[2]
        wb_marketplace.list_of_new_orders(call.message, WBToken, x_supplier_id, next, count)
    if calling_data[0] == 'Order menu':
        order_Id = calling_data[1]
        order_article = calling_data[2]
        wb_marketplace.order_menu(call.message, order_Id, order_article)
    if calling_data[0] == 'Changing supply to put order':
        order_Id = calling_data[1]
        order_article = calling_data[2]
        wb_marketplace.changing_supply_to_put_order(call.message, WBToken, x_supplier_id, order_Id, order_article)
    if calling_data[0] == 'Put order to supply':
        OrderList = [str(calling_data[2])]
        supply_Id = calling_data[1]
        wb_marketplace.put_order_to_supply(call.message, ApiToken, supply_Id, OrderList)
    if calling_data[0] == 'Order info':
        order_Id = calling_data[1]
        order_article = calling_data[2]
        wb_marketplace.order_info(call.message, ApiToken, order_Id, order_article)
    if calling_data[0] == 'Changing supply to put all orders':
        wb_marketplace.changing_supply_to_put_all_orders(call.message, WBToken, x_supplier_id)
    if calling_data[0] == 'Put all orders to supply':
        supply_Id = calling_data[1]
        OrderList = []
        wb_marketplace.put_all_orders_to_supply(call.message, ApiToken, supply_Id, OrderList)
    if calling_data[0] == 'Changing supply to put all orders by article':
        article = calling_data[1]
        wb_marketplace.changing_supply_to_put_all_orders_by_article(call.message, WBToken, x_supplier_id, article)
    if calling_data[0] == 'Put all orders by article to supply':
        supply_Id = calling_data[1]
        article = calling_data[2]
        OrderList = []
        wb_marketplace.put_all_orders_by_article_to_supply(call.message, ApiToken, WBToken, x_supplier_id, supply_Id, article, OrderList)

    if calling_data[0] == 'List of active supplies':
        wb_marketplace.list_of_active_supplies(call.message, WBToken, x_supplier_id)
    if calling_data[0] == 'Supply active menu':
        supply_Id = calling_data[1]
        wb_marketplace.supply_active_menu(call.message, supply_Id)
    if calling_data[0] == 'Supply close accept':
        supply_Id = calling_data[1]
        wb_marketplace.supply_close_accept(call.message, supply_Id)
    if calling_data[0] == 'Supply close':
        supply_Id = calling_data[1]
        wb_marketplace.supply_close(call.message, ApiToken, supply_Id)
    if calling_data[0] == 'Supply active info':
        supply_Id = calling_data[1]
        wb_marketplace.supply_active_info(call.message, ApiToken, supply_Id)
    if calling_data[0] == 'Create new supply':
        CreateSupply(call.message)
        for i in range(len(users_session)):
            if int(users_session[i]['id']) == call.message.chat.id:
                pointer_create = users_session[i]['pointer_create']
        while pointer_create != 1:
            for i in range(len(users_session)):
                if int(users_session[i]['id']) == call.message.chat.id:
                    pointer_create = users_session[i]['pointer_create']
                    name_create = users_session[i]['name_create']
            continue
        wb_marketplace.create_new_supply(call.message, WBToken, x_supplier_id, name_create)
        for i in range(len(users_session)):
            if int(users_session[i]['id']) == call.message.chat.id:
                users_session[i]['pointer_create'] = 0
                users_session[i]['name_create'] = 0

    if calling_data[0] == 'List of supplies on delivery':
        wb_marketplace.list_of_supplies_on_delivery(call.message, WBToken, x_supplier_id)
    if calling_data[0] == 'Supply closed menu':
        supply_Id = calling_data[1]
        wb_marketplace.supply_closed_menu(call.message, supply_Id)
    if calling_data[0] == 'Supply closed info':
        supply_Id = calling_data[1]
        wb_marketplace.supply_closed_info(call.message, WBToken, x_supplier_id, supply_Id)
    if calling_data[0] == 'Supply closed selection-sheet':
        supply_Id = calling_data[1]
        wb_marketplace.supply_closed_selection_sheet(call.message, ApiToken, WBToken, x_supplier_id, supply_Id)
    if calling_data[0] == 'Supply closed stickers':
        supply_Id = calling_data[1]
        wb_marketplace.supply_closed_stickers(call.message, ApiToken, WBToken, x_supplier_id, supply_Id)
    if calling_data[0] == 'Supply closed barcode':
        supply_Id = calling_data[1]
        wb_marketplace.supply_closed_barcode(call.message, WBToken, x_supplier_id, supply_Id)
    if calling_data[0] == 'Supply send documents':
        supply_Id = calling_data[1]
        wb_marketplace.supply_send_documents(call.message, ApiToken, RecipientId, WBToken, x_supplier_id, supply_Id, account_name)

    if calling_data[0] == 'Archive 100':
        next = calling_data[1]
        wb_marketplace.archive_100(call.message, WBToken, x_supplier_id, next)
    if calling_data[0] == 'Archive info':
        name = calling_data[1]
        wb_marketplace.archive_info(call.message, WBToken, x_supplier_id, name)
    if calling_data[0] == 'Supply archive selection-sheet':
        supply_Id = calling_data[1]
        wb_marketplace.supply_archive_selection_sheet(call.message, ApiToken, WBToken, x_supplier_id, supply_Id)
    if calling_data[0] == 'Supply archive stickers':
        supply_Id = calling_data[1]
        wb_marketplace.supply_archive_stickers(call.message, ApiToken, WBToken, x_supplier_id, supply_Id)


    if calling_data[0] == 'Statistics':
        wb_statistics.statistics(call.message, WBToken, x_supplier_id)
    if calling_data[0] == 'Statistic by warehouse':
        warehouse_name = calling_data[1]
        skip = calling_data[2]
        wb_statistics.statistic_by_warehouse(call.message, WBToken, x_supplier_id, warehouse_name, skip)
    if calling_data[0] == 'Stock info':
        barcode = calling_data[1]
        wb_statistics.stock_info(call.message, WBToken, x_supplier_id, barcode)
    if calling_data[0] == 'Change Stocks':
        barcode = calling_data[1]
        warehouse_id = calling_data[2]
        ChangeStocks(call.message)
        for i in range(len(users_session)):
            if int(users_session[i]['id']) == call.message.chat.id:
                pointer_stocks = users_session[i]['pointer_stocks']
                stock = users_session[i]['stock']
        while pointer_stocks != 1:
            for i in range(len(users_session)):
                if int(users_session[i]['id']) == call.message.chat.id:
                    pointer_stocks = users_session[i]['pointer_stocks']
                    stock = users_session[i]['stock']
            continue
        wb_statistics.change_stocks(call.message, WBToken, x_supplier_id, barcode, stock, warehouse_id)
        for i in range(len(users_session)):
            if int(users_session[i]['id']) == call.message.chat.id:
                users_session[i]['pointer_stocks'] = 0
                users_session[i]['stock'] = 0

    if calling_data[0] == 'Reviews':
        wb_reviews.reviews(call.message, WBToken, x_supplier_id)
    if calling_data[0] == 'Reviews samples':
        wb_reviews.reviews_sample(call.message)
    if calling_data[0] == 'Change sample':
        num = calling_data[1]
        wb_reviews.change_sample(call.message, account_name, account_reviews, num)
    if calling_data[0] == 'Changing sample':
        num = calling_data[1]
        if int(num) == 1:
            msg = bot.send_message(call.message.chat.id, 'Введите новый шаблон для отзыва ⭐: ')
            bot.register_next_step_handler(msg, sample_change_1)
        elif int(num) == 2:
            msg = bot.send_message(call.message.chat.id, 'Введите новый шаблон для отзыва ⭐⭐: ')
            bot.register_next_step_handler(msg, sample_change_2)
        elif int(num) == 3:
            msg = bot.send_message(call.message.chat.id, 'Введите новый шаблон для отзыва ⭐⭐⭐: ')
            bot.register_next_step_handler(msg, sample_change_3)
        elif int(num) == 4:
            msg = bot.send_message(call.message.chat.id, 'Введите новый шаблон для отзыва ⭐⭐⭐⭐: ')
            bot.register_next_step_handler(msg, sample_change_4)
        elif int(num) == 5:
            msg = bot.send_message(call.message.chat.id, 'Введите новый шаблон для отзыва ⭐⭐⭐⭐⭐: ')
            bot.register_next_step_handler(msg, sample_change_5)
        for i in range(len(users_session)):
            if int(users_session[i]['id']) == call.message.chat.id:
                pointer_create_sample = users_session[i]['pointer_create_sample']
        while pointer_create_sample != 1:
            for i in range(len(users_session)):
                if int(users_session[i]['id']) == call.message.chat.id:
                    pointer_create_sample = users_session[i]['pointer_create_sample']
            continue
        for i in range(len(users_session)):
            if int(users_session[i]['id']) == call.message.chat.id:
                users_session[i]['pointer_create_sample'] = 0
        init()
        wb_reviews.changing_sample(call.message)
    if calling_data[0] == 'Reviews Archive':
        wb_reviews.reviews_archive(call.message, WBToken, x_supplier_id)
    if calling_data[0] == 'Review archive info':
        id = calling_data[1]
        wb_reviews.reviews_archive_info(call.message, WBToken, x_supplier_id, id)
    if calling_data[0] == 'New reviews':
        wb_reviews.new_reviews(call.message, WBToken, x_supplier_id)
    if calling_data[0] == 'New review menu':
        id = calling_data[1]
        wb_reviews.new_review_menu(call.message, WBToken, x_supplier_id, id)
    if calling_data[0] == 'Review reply':
        id = calling_data[1]
        msg = bot.send_message(call.message.chat.id, '✏ Введите ответ на отзыв: ')
        bot.register_next_step_handler(msg, reply_to_review)
        for i in range(len(users_session)):
            if int(users_session[i]['id']) == call.message.chat.id:
                pointer_create = users_session[i]['pointer_create']
        while pointer_create != 1:
            for i in range(len(users_session)):
                if int(users_session[i]['id']) == call.message.chat.id:
                    pointer_create = users_session[i]['pointer_create']
                    name_create = users_session[i]['name_create']
            continue
        wb_reviews.patch_to_review(call.message, WBToken, x_supplier_id, id, name_create)
        for i in range(len(users_session)):
            if int(users_session[i]['id']) == call.message.chat.id:
                users_session[i]['pointer_create'] = 0
                users_session[i]['name_create'] = 0
    if calling_data[0] == 'Review reply by sample':
        id = calling_data[1]
        num = calling_data[2]
        for i in range(len(account_reviews)):
            if account_reviews[i]['name'] == account_name:
                if int(num) == 1:
                    text = account_reviews[i]['first']
                if int(num) == 2:
                    text = account_reviews[i]['second']
                if int(num) == 3:
                    text = account_reviews[i]['third']
                if int(num) == 4:
                    text = account_reviews[i]['fourth']
                if int(num) == 5:
                    text = account_reviews[i]['fifth']
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='✅ Да, ответить на отзыв по шаблону', callback_data=f'Reply to review|{id}|{num}')
        four = types.InlineKeyboardButton(text='🔙 Вернуться к отзыву', callback_data=f'New review menu|{id}')
        markup_inline.add(one, four)
        bot.send_message(call.message.chat.id, f'📝 Уверены, что хотите ответить на отзыв по шаблону:\n{text}', reply_markup=markup_inline)
    if calling_data[0] == 'Reply to review':
        id = calling_data[1]
        num = calling_data[2]
        for i in range(len(account_reviews)):
            if account_reviews[i]['name'] == account_name:
                if int(num) == 1:
                    text = account_reviews[i]['first']
                if int(num) == 2:
                    text = account_reviews[i]['second']
                if int(num) == 3:
                    text = account_reviews[i]['third']
                if int(num) == 4:
                    text = account_reviews[i]['fourth']
                if int(num) == 5:
                    text = account_reviews[i]['fifth']
        wb_reviews.patch_to_review(call.message, WBToken, x_supplier_id, id, text)

    if calling_data[0] == 'Advertising rates':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        one = types.InlineKeyboardButton(text='🗝 Поиск рекламных ставок по ключевому слову', callback_data='Advertising by keyword')
        two = types.InlineKeyboardButton(text='🧸 Поиск рекламных ставок по товару', callback_data='Advertising by good')
        three = types.InlineKeyboardButton(text='🛍 Поиск рекламных ставок по категории', callback_data='Advertising by category')
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(one, two, three, four)
        bot.send_message(call.message.chat.id, f'💸 Это рекламные ставки, здесь вы можете найти рекламные ставки по ключевым словам, товару и категории', reply_markup=markup_inline)
    if calling_data[0] == 'Advertising by keyword':
        msg = bot.send_message(call.message.chat.id, '🗝 Введите ключевое слово: ')
        bot.register_next_step_handler(msg, advertising_by_keyword)
    if calling_data[0] == 'Advertising by good':
        msg = bot.send_message(call.message.chat.id, '🧸 Введите ссылку на товар: ')
        bot.register_next_step_handler(msg, advertising_by_good)
    if calling_data[0] == 'Advertising by category':
        msg = bot.send_message(call.message.chat.id, '🛍 Введите ссылку на категорию: ')
        bot.register_next_step_handler(msg, advertising_by_category)

    if calling_data[0] == 'Changing account menu':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        three = types.InlineKeyboardButton(text='🔐 Изменить WB API-key', callback_data='Change Wilberries API-key')
        four = types.InlineKeyboardButton(text='📬 Изменить recipient-id', callback_data='Change recipient id')
        five = types.InlineKeyboardButton(text='📕 Изменить WBToken', callback_data='Change WBToken')
        six = types.InlineKeyboardButton(text='📗 Изменить x_supplier_id', callback_data='Change x_supplier_id')
        seven = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(three, four, five, six, seven)
        bot.send_message(call.message.chat.id, f'✏ Это изменение аккаунта, здесь вы можете поменять уникальные идентификаторы аккаунта и rec-id менеджера поставок', reply_markup=markup_inline)
    if calling_data[0] == 'Change Wilberries API-key':
        wb_account.change_wb_api(call.message, ApiToken)
    if calling_data[0] == 'Change API-key':
        msg = bot.send_message(call.message.chat.id, '🔐 Введите новый Wildberries API: ')
        bot.register_next_step_handler(msg, WbbApi)
    if calling_data[0] == 'Change recipient id':
        wb_account.change_rec_id(call.message, RecipientId)
    if calling_data[0] == 'Changing rec-id':
        msg = bot.send_message(call.message.chat.id, '📬 Введите новый recipient-id:')
        bot.register_next_step_handler(msg, RefererChoice1)
    if calling_data[0] == 'Change WBToken':
        wb_account.change_wb_token(call.message, WBToken)
    if calling_data[0] == 'Change WBT':
        msg = bot.send_message(call.message.chat.id, '📕 Введите новый WBToken: ')
        bot.register_next_step_handler(msg, WbbWBT)
    if calling_data[0] == 'Change x_supplier_id':
        wb_account.change_sup_id(call.message, x_supplier_id)
    if calling_data[0] == 'Change x_sup':
        msg = bot.send_message(call.message.chat.id, '📗 Введите новый x_supplier_id: ')
        bot.register_next_step_handler(msg, WbbXSP)

    if calling_data[0] == 'Account menu':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        one = types.InlineKeyboardButton(text='♻ Изменить аккаунт', callback_data='Change account')
        two = types.InlineKeyboardButton(text='✏ Добавить аккаунт', callback_data='Add account')
        three = types.InlineKeyboardButton(text='🗑 Удалить аккаунт', callback_data='Delete account')
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(one, two, three, four)
        bot.send_message(call.message.chat.id, f'⚙ Это управление аккаунтами, здесь вы можете настроить свои аккаунты wb-partner', reply_markup=markup_inline)
    if calling_data[0] == 'Change account':
        wb_account.change_account(call.message, wb_accounts)
    if calling_data[0] == 'Changing account':
        id = calling_data[1]
        change_account(call.message.chat.id, id)
        wb_account.changing_account(call.message, id)
    if calling_data[0] == 'Add account':
        create_account_1(call.message)
    if calling_data[0] == 'Delete account':
        wb_account.delete_account(call.message, wb_accounts)
    if calling_data[0] == 'Deliting account':
        name = calling_data[1]
        wb_account.deliting_account(call.message, name)
        init()
        init_session()

    if calling_data[0] == 'adm':
        adm_1(call.message)
    if calling_data[0] == 'changelog':
        wb_changelog.changelog(call.message)

    if calling_data[0] == 'manual':
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад в главное меню', callback_data='main')
        markup_inline.add(one)
        bot.send_document(call.message.chat.id, open(r'manual.pdf', 'rb'), reply_markup=markup_inline)

bot.polling(none_stop=True, timeout=0)
