import telebot
from telebot import types
import io
import csv
import WBApi as wb_market

bot = telebot.TeleBot('')

def statistics(message, WBToken, x_supplier_id):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    jsn = wb_market.GetWarehouses(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        markup_list = []
        for i in range(len(jsn['data'])):
            Warehouse = {
                'name': jsn['data'][i]['name'],
                'id': jsn['data'][i]['id']
            }
            markup_list.append(types.InlineKeyboardButton(text=f'{i + 1}: 🏗 {Warehouse["name"]}', callback_data=f'Statistic by warehouse|{Warehouse["name"]}|0'))
        for i in range(len(markup_list)):
            markup_inline.add(markup_list[i])
        one = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(one)
        bot.send_message(message.chat.id, f'📊 Это раздел управления остатками, здесь вы можете редактировать количество товара на складах\n🏗 Список складов ({len(markup_list)}):', reply_markup=markup_inline)

def statistic_by_warehouse(message, WBToken, x_supplier_id, warehouse_name, skip):
    skip = int(skip)
    jsn = wb_market.GetStocks(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        markup_list = []
        for i in range(len(jsn['data']['stocks'])):
            article = jsn['data']['stocks'][i]['article']
            if jsn['data']['stocks'][i]['warehouseName'] == warehouse_name:
                barcode = jsn["data"]["stocks"][i]["barcode"]
                markup_list.append(
                    types.InlineKeyboardButton(text=f'{i + 1}: 🛒 {article} ({jsn["data"]["stocks"][i]["stock"]})',
                                               callback_data=f'Stock info|{barcode}'))
        if len(markup_list) > skip + 10:
            for i in range(skip, skip + 10):
                markup_inline.add(markup_list[i])
            three = types.InlineKeyboardButton(text='🔄 Следующая страница 🔄', callback_data=f'Statistic by warehouse|{warehouse_name}|{skip + 10}')
        else:
            for i in range(skip, len(markup_list)):
                markup_inline.add(markup_list[i])
            three = types.InlineKeyboardButton(text='🔄 Следующая страница 🔄', callback_data=f'Statistic by warehouse|{warehouse_name}|0')
        one = types.InlineKeyboardButton(text='🔙 Вернуться меню складов', callback_data='Statistics')
        markup_inline.add(three)
        markup_inline.add(one)
        print(skip)
        if skip == 0:
            bot.send_message(message.chat.id, f'🛒 Список предметов на складе ({warehouse_name}):', reply_markup=markup_inline)
        else:
            bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup_inline)

def stock_info(message, WBToken, x_supplier_id, barcode):
    Stockjsn = 0
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    jsn = wb_market.GetStocks(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['data']['stocks'])):
            if jsn['data']['stocks'][i]['barcode'] == barcode:
                Stockjsn = jsn['data']['stocks'][i]
        two = types.InlineKeyboardButton(text='⚙ Изменить кол-во товара',
                                         callback_data=f'Change Stocks|{barcode}|{Stockjsn["warehouseId"]}')
        one = types.InlineKeyboardButton(text='🔙 Вернуться в меню склада',
                                         callback_data=f'Statistic by warehouse|{Stockjsn["warehouseName"]}|0')
        markup_inline.add(two, one)
        bot.send_message(message.chat.id, f'🛒 Информация по предмету {Stockjsn["name"]}:',
                         reply_markup=markup_inline)

def change_stocks(message, WBToken, x_supplier_id, barcode, stock, warehouse_id):
    jsn = wb_market.PostChangeStocks(barcode, int(stock), int(warehouse_id), WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        four = types.InlineKeyboardButton(text='🔙 Назад к информации по товару', callback_data=f'Stock info|{barcode}')
        markup_inline.add(four)
        bot.send_message(message.chat.id, f'✅ Количество товара успешно изменено', reply_markup=markup_inline)