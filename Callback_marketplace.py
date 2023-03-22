import telebot
from telebot import types
import io
import csv
import WBApi as wb_market

bot = telebot.TeleBot('')

#Функция для отображения меню маркетплейса
def marketplace(message, WBToken, x_supplier_id):
    jsn1 = wb_market.GetOrdersNewCount(WBToken, x_supplier_id)
    jsn2 = wb_market.Alternative_GetSuppliesInWork(WBToken, x_supplier_id)
    jsn3 = wb_market.Alternative_GetSuppliesOnDelivery(WBToken, x_supplier_id)
    jsn4 = wb_market.GetSuppliesFromArhive(WBToken, x_supplier_id, 0, 1000)
    if jsn1 == 'error' or jsn2 == 'error' or jsn3 == 'error' or jsn4 == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text=f'🔔 Новые заказы ({jsn1["data"]["fbs"]})',
                                         callback_data='List of new orders|0|0')
        two = types.InlineKeyboardButton(text=f'📦 Поставки на сборке ({len(jsn2["data"]["supplies"])})',
                                         callback_data='List of active supplies')
        three = types.InlineKeyboardButton(text=f'🚚 Закрытые поставки ({len(jsn3["data"]["supplies"])})',
                                           callback_data='List of supplies on delivery')
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        five = types.InlineKeyboardButton(text=f'🗃 Архив поставок ({len(jsn4["data"]["supplies"])})',
                                          callback_data='Archive 100|0')
        markup_inline.add(one)
        markup_inline.add(two)
        markup_inline.add(three)
        markup_inline.add(five, four)
        bot.send_message(message.chat.id, '📈 Маркетплейс 📉 - здесь вы можете управлять своими заказами и поставками', reply_markup=markup_inline)

#Функции для меню новых заказов
def list_of_new_orders(message, WBToken, x_supplier_id, now, count):
    NewOrdersList = []
    jsn = wb_market.Alternative_GetOrdersNew(WBToken, x_supplier_id, now)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['data']['orders'])):
            NewOrder = {
                'orderId': jsn['data']['orders'][i]['id'],
                'article': jsn['data']['orders'][i]['article']
            }
            NewOrdersList.append(NewOrder)
        markup_inline = types.InlineKeyboardMarkup()
        markup_list = []
        if count == '50':
            for i in range(50, len(NewOrdersList)):
                markup_list.append(
                    types.InlineKeyboardButton(
                        text=f'{i - 49}: 🔔 {NewOrdersList[i]["orderId"]} "{NewOrdersList[i]["article"]}"',
                        callback_data=f'Order menu|{NewOrdersList[i]["orderId"]}|{NewOrdersList[i]["article"]}'))
        else:
            if len(NewOrdersList) >= 51:
                for i in range(0, 50):
                    markup_list.append(
                        types.InlineKeyboardButton(
                            text=f'{i + 1}: 🔔 {NewOrdersList[i]["orderId"]} "{NewOrdersList[i]["article"]}"',
                            callback_data=f'Order menu|{NewOrdersList[i]["orderId"]}|{NewOrdersList[i]["article"]}'))
            else:
                for i in range(0, len(NewOrdersList)):
                    markup_list.append(
                        types.InlineKeyboardButton(
                            text=f'{i + 1}: 🔔 {NewOrdersList[i]["orderId"]} "{NewOrdersList[i]["article"]}"',
                            callback_data=f'Order menu|{NewOrdersList[i]["orderId"]}|{NewOrdersList[i]["article"]}'))
        for i in range(len(markup_list)):
            markup_inline.add(markup_list[i])

        if count == '0' and len(NewOrdersList) < 50:
            now_1 = jsn['data']['next']
        elif count == '0':
            now_1 = now
        else:
            now_1 = jsn['data']['next']

        if count == '0' and len(NewOrdersList) > 50:
            three = types.InlineKeyboardButton(text='🔄 Следующая страница 🔄',
                                               callback_data=f'List of new orders|{now_1}|50')
        else:
            three = types.InlineKeyboardButton(text='🔄 Следующая страница 🔄',
                                               callback_data=f'List of new orders|{now_1}|0')
        one = types.InlineKeyboardButton(text='📦 Перевести все заказы на сборку',
                                         callback_data='Changing supply to put all orders')
        two = types.InlineKeyboardButton(text='🔙 Назад в Маркетплейс', callback_data='Marketplace')
        markup_inline.add(three)
        markup_inline.add(one)
        markup_inline.add(two)
        if now_1 == 0:
            bot.send_message(message.chat.id, f'🔔 Список новых заказов ({len(NewOrdersList)}):', reply_markup=markup_inline)
        else:
            bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id,
                                          reply_markup=markup_inline)

def order_menu(message, order_Id, order_article):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    one = types.InlineKeyboardButton(text='📦 Прикрепить заказ к поставке',
                                     callback_data=f'Changing supply to put order|{order_Id}|{order_article}')
    four = types.InlineKeyboardButton(text='📦 Прикрепить все заказы с этим артикулом к поставке', callback_data=f'Changing supply to put all orders by article|{order_article}')
    two = types.InlineKeyboardButton(text='ℹ️Вывод подробной информации по заказу',
                                     callback_data=f'Order info|{order_Id}|{order_article}')
    three = types.InlineKeyboardButton(text='🔙 Назад к списку заказов', callback_data='List of new orders|0|0')
    markup_inline.add(one, four, two, three)
    bot.send_message(message.chat.id, f'🔔 Заказ № {order_Id} "{order_article}"', reply_markup=markup_inline)

def changing_supply_to_put_order(message, WBToken, x_supplier_id, order_Id, order_article):
    ActiveSuppliesList = []
    jsn = wb_market.Alternative_GetSuppliesInWork(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['data']['supplies'])):
            ActiveSupply = {
                'supplyId': jsn['data']['supplies'][i]['supplyID'],
                'name': jsn['data']['supplies'][i]['name']
            }
            ActiveSuppliesList.append(ActiveSupply)
        markup_inline = types.InlineKeyboardMarkup()
        markup_list = []
        for i in range(0, len(ActiveSuppliesList)):
            markup_list.append(types.InlineKeyboardButton(
                text=f'{i + 1}: 📦 {ActiveSuppliesList[i]["supplyId"]} "{ActiveSuppliesList[i]["name"]}"',
                callback_data=f'Put order to supply|{ActiveSuppliesList[i]["supplyId"]}|{order_Id}'))
        for i in range(len(markup_list)):
            markup_inline.add(markup_list[i])
        one = types.InlineKeyboardButton(text='🔙 Назад к заказу',
                                         callback_data=f'Order menu|{order_Id}|{order_article}')
        markup_inline.add(one)
        bot.send_message(message.chat.id, f'📦 Выберите поставку из списка (total - {len(ActiveSuppliesList)}):',
                         reply_markup=markup_inline)

def put_order_to_supply(message, ApiToken, supply_Id, OrderList):
    jsn = wb_market.PutOrdersToSupply(ApiToken, supply_Id, OrderList)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад к списку заказов', callback_data='List of new orders|0|0')
        markup_inline.add(one)
        bot.send_message(message.chat.id, f'✅ Заказ {OrderList[0]} успешно прикреплен к поставке № {supply_Id}',
                         reply_markup=markup_inline)

def order_info(message, ApiToken, order_Id, order_article):
    OrderDict = 0
    jsn = wb_market.GetOrdersNew(ApiToken)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        for i in range(len(jsn['orders'])):
            if jsn['orders'][i]['orderId'] == order_Id:
                OrderDict = jsn['orders'][i]
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад к заказу', callback_data=f'Order menu|{order_Id}|{order_article}')
        markup_inline.add(one)
        bot.send_message(message.chat.id, f'Идентификатор заказа: {OrderDict["orderId"]}\nДата создания: {OrderDict["dateCreated"][0:10]}\nИдентификатор артикула: {OrderDict["chrtId"]}\nШтрихкод товара: {OrderDict["barcode"]}', reply_markup=markup_inline)

def changing_supply_to_put_all_orders(message, WBToken, x_supplier_id):
    ActiveSuppliesList = []
    jsn = wb_market.Alternative_GetSuppliesInWork(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        for i in range(len(jsn['data']['supplies'])):
            ActiveSupply = {
                'supplyId': jsn['data']['supplies'][i]['supplyID'],
                'name': jsn['data']['supplies'][i]['name']
            }
            ActiveSuppliesList.append(ActiveSupply)
        markup_inline = types.InlineKeyboardMarkup()
        markup_list = []
        for i in range(0, len(ActiveSuppliesList)):
            markup_list.append(types.InlineKeyboardButton(text=f'{i + 1}: 📦 {ActiveSuppliesList[i]["supplyId"]} "{ActiveSuppliesList[i]["name"]}"', callback_data=f'Put all orders to supply|{ActiveSuppliesList[i]["supplyId"]}'))
        for i in range(len(markup_list)):
            markup_inline.add(markup_list[i])
        one = types.InlineKeyboardButton(text='🔙 Назад к списку заказов', callback_data='List of new orders|0|0')
        markup_inline.add(one)
        bot.send_message(message.chat.id, f'📦 Выберите поставку из списка (total - {len(ActiveSuppliesList)}):', reply_markup=markup_inline)

def put_all_orders_to_supply(message, ApiToken, supply_Id, OrderList):
    jsn = wb_market.GetOrdersNew(ApiToken)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['orders'])):
            OrderList.append(str(jsn['orders'][i]['orderId']))
    jsn1 = wb_market.PutOrdersToSupply(ApiToken, supply_Id, OrderList)
    if jsn1 == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад к списку заказов', callback_data='List of new orders|0|0')
        markup_inline.add(one)
        bot.send_message(message.chat.id, f'✅ Все заказы успешно прикреплен к поставке № {supply_Id}',
                         reply_markup=markup_inline)

def changing_supply_to_put_all_orders_by_article(message, WBToken, x_supplier_id, article):
    ActiveSuppliesList = []
    jsn = wb_market.Alternative_GetSuppliesInWork(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        for i in range(len(jsn['data']['supplies'])):
            ActiveSupply = {
                'supplyId': jsn['data']['supplies'][i]['supplyID'],
                'name': jsn['data']['supplies'][i]['name']
            }
            ActiveSuppliesList.append(ActiveSupply)
        markup_inline = types.InlineKeyboardMarkup()
        markup_list = []
        for i in range(0, len(ActiveSuppliesList)):
            markup_list.append(types.InlineKeyboardButton(text=f'{i + 1}: 📦 {ActiveSuppliesList[i]["supplyId"]} "{ActiveSuppliesList[i]["name"]}"', callback_data=f'Put all orders by article to supply|{ActiveSuppliesList[i]["supplyId"]}|{article}'))
        for i in range(len(markup_list)):
            markup_inline.add(markup_list[i])
        one = types.InlineKeyboardButton(text='🔙 Назад к списку заказов', callback_data='List of new orders|0|0')
        markup_inline.add(one)
        bot.send_message(message.chat.id, f'📦 Выберите поставку из списка (total - {len(ActiveSuppliesList)}):', reply_markup=markup_inline)

def put_all_orders_by_article_to_supply(message, ApiToken, WBToken, x_supplier_id, supply_Id, article, OrderList):
    jsn = wb_market.Alternative_GetOrdersNew_1000(WBToken, x_supplier_id, 0)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['data']['orders'])):
            if jsn['data']['orders'][i]['article'] == article:
                OrderList.append(str(jsn['data']['orders'][i]['id']))
    jsn1 = wb_market.PutOrdersToSupply(ApiToken, supply_Id, OrderList)
    if jsn1 == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад к списку заказов', callback_data='List of new orders|0|0')
        markup_inline.add(one)
        bot.send_message(message.chat.id, f'✅ Все заказы c артикулом {article} успешно прикреплены к поставке № {supply_Id}',
                         reply_markup=markup_inline)
#Функции для меню поставок в сборке
def list_of_active_supplies(message, WBToken, x_supplier_id):
    ActiveSuppliesList = []
    jsn = wb_market.Alternative_GetSuppliesInWork(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['data']['supplies'])):
            ActiveSupply = {
                'supplyId': jsn['data']['supplies'][i]['supplyID'],
                'name': jsn['data']['supplies'][i]['name']
            }
            ActiveSuppliesList.append(ActiveSupply)
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        markup_list = []
        for i in range(0, len(ActiveSuppliesList)):
            markup_list.append(types.InlineKeyboardButton(
                text=f'{i + 1}: 📦 {ActiveSuppliesList[i]["supplyId"]} "{ActiveSuppliesList[i]["name"]}"',
                callback_data=f'Supply active menu|{ActiveSuppliesList[i]["supplyId"]}'))
        for i in range(len(markup_list)):
            markup_inline.add(markup_list[i])
        two = types.InlineKeyboardButton(text='✏ Создать новую поставку', callback_data='Create new supply')
        one = types.InlineKeyboardButton(text='🔙 Назад в Маркетплейс', callback_data='Marketplace')
        markup_inline.add(two, one)
        bot.send_message(message.chat.id, f'📦 Список поставок на сборке ({len(ActiveSuppliesList)}):',
                         reply_markup=markup_inline)

def supply_active_menu(message, supply_Id):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    one = types.InlineKeyboardButton(text='🚚 Перевести поставку на доставку',
                                     callback_data=f'Supply close accept|{supply_Id}')
    three = types.InlineKeyboardButton(text='📋 Вывод информации по поставке',
                                       callback_data=f'Supply active info|{supply_Id}')
    four = types.InlineKeyboardButton(text='🔙 Назад к списку поставок в сборке',
                                      callback_data='List of active supplies')
    markup_inline.add(one, three, four)
    bot.send_message(message.chat.id, f'📦 Поставка № {supply_Id}', reply_markup=markup_inline)

def supply_close_accept(message, supply_Id):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    one = types.InlineKeyboardButton(text=f'✅ Да, закрыть поставку № {supply_Id}',
                                     callback_data=f'Supply close|{supply_Id}')
    four = types.InlineKeyboardButton(text='🔙 Назад к списку поставок в сборке',
                                      callback_data='List of active supplies')
    markup_inline.add(one, four)
    bot.send_message(message.chat.id, f'📦 Поставка № {supply_Id}', reply_markup=markup_inline)

def supply_close(message, ApiToken, supply_Id):
    jsn = wb_market.PostSupplyClose(ApiToken, supply_Id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        four = types.InlineKeyboardButton(text='🔙 Вернуться к списку поставок в сборке',
                                          callback_data='List of active supplies')
        markup_inline.add(four)
        bot.send_message(message.chat.id, f'✅ Поставка № {supply_Id} успешно закрыта', reply_markup=markup_inline)

def supply_active_info(message, ApiToken, supply_Id):
    ActiveSupplyOrderList = []
    jsn = wb_market.GetOrdersBySupply(ApiToken, supply_Id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['orders'])):
            ActiveSupplyOrderList.append(jsn['orders'][i]['orderId'])
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад в меню поставки',
                                         callback_data=f'Supply active menu|{supply_Id}')
        markup_inline.add(one)
        bot.send_message(message.chat.id,
                         f'Количество заказов в поставке: {len(ActiveSupplyOrderList)}\nСписок заказов в поставке:\n {ActiveSupplyOrderList[::]}',
                         reply_markup=markup_inline)

def create_new_supply(message, WBToken, x_supplier_id, name_create):
    jsn = wb_market.PostCreateNewSupply(name_create, WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        four = types.InlineKeyboardButton(text='🔙 Назад к списку поставок в сборке',
                                          callback_data='List of active supplies')
        markup_inline.add(four)
        bot.send_message(message.chat.id, f'✅ Поставка успешно создана', reply_markup=markup_inline)

#Функции для меню поставок в доставке
def list_of_supplies_on_delivery(message, WBToken, x_supplier_id):
    OnDeliverySuppliesList = []
    jsn = wb_market.Alternative_GetSuppliesOnDelivery(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['data']['supplies'])):
            OnDeliverySupply = {
                'supplyId': jsn['data']['supplies'][i]['supplyID'],
                'name': jsn['data']['supplies'][i]['name']
            }
            OnDeliverySuppliesList.append(OnDeliverySupply)
        markup_inline = types.InlineKeyboardMarkup()
        markup_list = []
        for i in range(0, len(OnDeliverySuppliesList)):
            markup_list.append(types.InlineKeyboardButton(
                text=f'{i + 1}: 🚚 {OnDeliverySuppliesList[i]["supplyId"]} "{OnDeliverySuppliesList[i]["name"]}"',
                callback_data=f'Supply closed menu|{OnDeliverySuppliesList[i]["supplyId"]}'))
        for i in range(len(markup_list)):
            markup_inline.add(markup_list[i])
        one = types.InlineKeyboardButton(text='🔙 Назад в Маркетплейс', callback_data='Marketplace')
        markup_inline.add(one)
        bot.send_message(message.chat.id, f'🚚 Список закрытых поставок ({len(OnDeliverySuppliesList)}):',
                         reply_markup=markup_inline)

def supply_closed_menu(message, supply_Id):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    one = types.InlineKeyboardButton(text='ℹ Вывод информации по поставке',
                                     callback_data=f'Supply closed info|{supply_Id}')
    two = types.InlineKeyboardButton(text='📋 Получить лист подбора по поставке',
                                     callback_data=f'Supply closed selection-sheet|{supply_Id}')
    three = types.InlineKeyboardButton(text='📋 Получить этикетки по поставке',
                                       callback_data=f'Supply closed stickers|{supply_Id}')
    four = types.InlineKeyboardButton(text='📋 Получить баркод по поставке',
                                      callback_data=f'Supply closed barcode|{supply_Id}')
    five = types.InlineKeyboardButton(text='📬 Отправить документы по поставке',
                                      callback_data=f'Supply send documents|{supply_Id}')
    six = types.InlineKeyboardButton(text='🔙 Назад к списку закрытых поставок',
                                     callback_data='List of supplies on delivery')
    markup_inline.add(one, two, three, four, five, six)
    bot.send_message(message.chat.id, f'🚚 Поставка № {supply_Id}', reply_markup=markup_inline)

def supply_closed_info(message, WBToken, x_supplier_id, supply_Id):
    ArchiveSupply = 0
    jsn = wb_market.Alternative_GetSuppliesOnDelivery(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['data']['supplies'])):
            if jsn['data']['supplies'][i]['supplyID'] == supply_Id:
                ArchiveSupply = jsn['data']['supplies'][i]
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад в меню поставки',
                                         callback_data=f'Supply closed menu|{supply_Id}')
        markup_inline.add(one)
        bot.send_message(message.chat.id,
                         f'Название поставки: {ArchiveSupply["name"]}\nИдентификатор поставки: {ArchiveSupply["supplyID"]}\nСтатус поставки: {ArchiveSupply["state"]["code"]} | {ArchiveSupply["state"]["title"]}\nВремя создания поставки: {ArchiveSupply["createdAt"]}\nВремя сканирования штрихкода: {ArchiveSupply["scannedAt"]}\nКоличество товаров: {ArchiveSupply["ordersCnt"]}\nКоличество товаров на повторную отправку: {ArchiveSupply["reshipmentOrdersCnt"]}',
                         reply_markup=markup_inline)

def supply_closed_selection_sheet(message, ApiToken, WBToken, x_supplier_id, supply_Id):
    ActiveSupplyOrderList = []
    jsn = wb_market.GetOrdersBySupply(ApiToken, supply_Id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['orders'])):
            ActiveSupplyOrderList.append(int(jsn['orders'][i]['orderId']))
    jsn1 = wb_market.WritePdfSelectionSheet(supply_Id, ActiveSupplyOrderList, WBToken, x_supplier_id)
    if jsn1 == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад в меню поставки',
                                         callback_data=f'Supply closed menu|{supply_Id}')
        markup_inline.add(one)
        bot.send_document(message.chat.id, open(r'selection_sheet.pdf', 'rb'), reply_markup=markup_inline)

def supply_closed_stickers(message, ApiToken, WBToken, x_supplier_id, supply_Id):
    ActiveSupplyOrderList = []
    jsn = wb_market.GetOrdersBySupply(ApiToken, supply_Id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['orders'])):
            ActiveSupplyOrderList.append(int(jsn['orders'][i]['orderId']))
    jsn1 = wb_market.WritePdfStickers(ActiveSupplyOrderList, WBToken, x_supplier_id)
    if jsn1 == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад в меню поставки',
                                         callback_data=f'Supply closed menu|{supply_Id}')
        markup_inline.add(one)
        bot.send_document(message.chat.id, open(r'stickers.pdf', 'rb'), reply_markup=markup_inline)

def supply_closed_barcode(message, WBToken, x_supplier_id, supply_Id):
    jsn = wb_market.WritePdfBarcode(supply_Id, WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад в меню поставки',
                                         callback_data=f'Supply closed menu|{supply_Id}')
        markup_inline.add(one)
        bot.send_document(message.chat.id, open(r'barcode.pdf', 'rb'), reply_markup=markup_inline)

def supply_send_documents(message, ApiToken, RecipientId, WBToken, x_supplier_id, supply_Id, account_name):
    bot.send_message(RecipientId, f'Документы для поставки № {supply_Id} от {account_name}')
    ActiveSupplyOrderList = []
    jsn = wb_market.GetOrdersBySupply(ApiToken, supply_Id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        for i in range(len(jsn['orders'])):
            ActiveSupplyOrderList.append(int(jsn['orders'][i]['orderId']))
    jsn1 = wb_market.WritePdfSelectionSheet(supply_Id, ActiveSupplyOrderList, WBToken, x_supplier_id)
    jsn2 = wb_market.WritePdfStickers(ActiveSupplyOrderList, WBToken, x_supplier_id)
    jsn3 = wb_market.WritePdfBarcode(supply_Id, WBToken, x_supplier_id)
    if jsn1 == 'error' or jsn2 == 'error' or jsn3 == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        bot.send_media_group(RecipientId, [types.InputMediaDocument(open(r'selection_sheet.pdf', 'rb')),
                                           types.InputMediaDocument(open(r'stickers.pdf', 'rb')),
                                           types.InputMediaDocument(open(r'barcode.pdf', 'rb'))])
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад в меню поставки', callback_data=f'Supply closed menu|{supply_Id}')
        markup_inline.add(one)
        bot.send_message(message.chat.id, f'✅ Документы для поставки № {supply_Id} успешно отправлены', reply_markup=markup_inline)

#Функции для меню архив
def archive_100(message, WBToken, x_supplier_id, now):
    jsn = wb_market.GetSuppliesFromArhive(WBToken, x_supplier_id, now, 10)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        ArchiveSupplyList = []
        for i in range(len(jsn['data']['supplies'])):
            ArchiveSupplyList.append(jsn['data']['supplies'][i]['name'])
        next = jsn['data']['next']
        markup_inline = types.InlineKeyboardMarkup()
        markup_list = []
        if len(ArchiveSupplyList) >= 99:
            for i in range(0, 99):
                markup_list.append(types.InlineKeyboardButton(text=f'{i + 1}: 🗃 "{ArchiveSupplyList[i]}"',
                                                              callback_data=f'Archive info|{jsn["data"]["supplies"][i]["supplyID"]}'))
        else:
            for i in range(0, len(ArchiveSupplyList)):
                markup_list.append(types.InlineKeyboardButton(text=f'{i + 1}: 🗃 "{ArchiveSupplyList[i]}"',
                                                              callback_data=f'Archive info|{jsn["data"]["supplies"][i]["supplyID"]}'))
        for i in range(len(markup_list)):
            markup_inline.add(markup_list[i])
        three = types.InlineKeyboardButton(text='🔄 Следующая страница 🔄', callback_data=f'Archive 100|{next}')
        one = types.InlineKeyboardButton(text='🔙 Назад в Маркетплейс', callback_data='Marketplace')
        markup_inline.add(three)
        markup_inline.add(one)
        if now == '0':
            bot.send_message(message.chat.id, f'🗃 Архив поставок:', reply_markup=markup_inline)
        else:
            bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup_inline)

def archive_info(message, WBToken, x_supplier_id, name):
    jsn = wb_market.GetSuppliesFromArhive(WBToken, x_supplier_id, 0, 1000)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        ArchiveSupply = 0
        for i in range(len(jsn['data']['supplies'])):
            if name == jsn['data']['supplies'][i]['supplyID']:
                ArchiveSupply = jsn['data']['supplies'][i]
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        two = types.InlineKeyboardButton(text='📋 Получить лист подбора по поставке', callback_data=f'Supply archive selection-sheet|{ArchiveSupply["supplyID"]}')
        three = types.InlineKeyboardButton(text='📋 Получить этикетки по поставке', callback_data=f'Supply archive stickers|{ArchiveSupply["supplyID"]}')
        one = types.InlineKeyboardButton(text='🔙 Назад в Архив', callback_data='Archive 100|0')
        markup_inline.add(two, three, one)
        bot.send_message(message.chat.id, f'🗃\nНазвание поставки: {ArchiveSupply["name"]}\nИдентификатор поставки: {ArchiveSupply["supplyID"]}\nСтатус поставки: {ArchiveSupply["state"]["code"]} | {ArchiveSupply["state"]["title"]}\nВремя создания поставки: {ArchiveSupply["createdAt"]}\nВремя сканирования штрихкода: {ArchiveSupply["scannedAt"]}\nКоличество товаров: {ArchiveSupply["ordersCnt"]}\nКоличество товаров на повторную отправку: {ArchiveSupply["reshipmentOrdersCnt"]}', reply_markup=markup_inline)

def supply_archive_selection_sheet(message, ApiToken, WBToken, x_supplier_id, supply_Id):
    ActiveSupplyOrderList = []
    jsn = wb_market.GetOrdersBySupply(ApiToken, supply_Id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        for i in range(len(jsn['orders'])):
            ActiveSupplyOrderList.append(int(jsn['orders'][i]['orderId']))
    jsn1 = wb_market.WritePdfSelectionSheet(supply_Id, ActiveSupplyOrderList, WBToken, x_supplier_id)
    if jsn1 == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад в архив', callback_data='Archive 100|0')
        markup_inline.add(one)
        bot.send_document(message.chat.id, open(r'selection_sheet.pdf', 'rb'), reply_markup=markup_inline)

def supply_archive_stickers(message, ApiToken, WBToken, x_supplier_id, supply_Id):
    ActiveSupplyOrderList = []
    jsn = wb_market.GetOrdersBySupply(ApiToken, supply_Id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['orders'])):
            ActiveSupplyOrderList.append(int(jsn['orders'][i]['orderId']))
    jsn1 = wb_market.WritePdfStickers(ActiveSupplyOrderList, WBToken, x_supplier_id)
    if jsn1 == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад в архив', callback_data='Archive 100|0')
        markup_inline.add(one)
        bot.send_document(message.chat.id, open(r'stickers.pdf', 'rb'), reply_markup=markup_inline)