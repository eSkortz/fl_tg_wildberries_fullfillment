import telebot
from telebot import types
import io
import csv
import WBApi as wb_market

bot = telebot.TeleBot('')

def reviews(message, WBToken, x_supplier_id):
    jsn = wb_market.GetReviews(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        one = types.InlineKeyboardButton(text=f'📣 Новые отзывы ({jsn["data"]["countUnanswered"]})', callback_data='New reviews')
        two = types.InlineKeyboardButton(text=f'🗃 Архив отзывов ({jsn["data"]["countArchive"]})', callback_data='Reviews Archive')
        three = types.InlineKeyboardButton(text=f'📝 Шаблоны для ответа', callback_data='Reviews samples')
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(one, two, three, four)
        bot.send_message(message.chat.id, '💬 Это раздел отзывов здесь вы можете отвечать на отзывы, в том числе с помощью шаблонов', reply_markup=markup_inline)

def reviews_sample(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    one = types.InlineKeyboardButton(text='⭐', callback_data='Change sample|1')
    two = types.InlineKeyboardButton(text='⭐⭐', callback_data='Change sample|2')
    three = types.InlineKeyboardButton(text='⭐⭐⭐', callback_data='Change sample|3')
    four = types.InlineKeyboardButton(text='⭐⭐⭐⭐', callback_data='Change sample|4')
    five = types.InlineKeyboardButton(text='⭐⭐⭐⭐⭐', callback_data='Change sample|5')
    six = types.InlineKeyboardButton(text='🔙 Вернуться в отзывы', callback_data='Reviews')
    markup_inline.add(one, two, three, four, five, six)
    bot.send_message(message.chat.id, '📝 Шаблоны для отзывов', reply_markup=markup_inline)

def change_sample(message, account_name, account_reviews, num):
    num = int(num)
    for i in range(len(account_reviews)):
        if account_reviews[i]['name'] == account_name:
            if num == 1:
                sample_to_change = account_reviews[i]['first']
            if num == 2:
                sample_to_change = account_reviews[i]['second']
            if num == 3:
                sample_to_change = account_reviews[i]['third']
            if num == 4:
                sample_to_change = account_reviews[i]['fourth']
            if num == 5:
                sample_to_change = account_reviews[i]['fifth']
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    one = types.InlineKeyboardButton(text='⚙ Изменить шаблон', callback_data=f'Changing sample|{num}')
    two = types.InlineKeyboardButton(text='🔙 Вернуться в шаблоны', callback_data='Reviews samples')
    markup_inline.add(one, two)
    stars = '⭐'*num
    bot.send_message(message.chat.id, f'Ваш шаблон для отзыва {stars}:\n{sample_to_change}', reply_markup=markup_inline)

def changing_sample(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    two = types.InlineKeyboardButton(text='🔙 Вернуться в шаблоны', callback_data='Reviews samples')
    markup_inline.add(two)
    bot.send_message(message.chat.id, f'✅ Шаблон для отзыва успешно изменен', reply_markup=markup_inline)

def reviews_archive(message, WBToken, x_supplier_id):
    jsn = wb_market.GetArchiveReviews(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        markup_list = []
        for i in range(len(jsn['data']['feedbacks'])):
            stars = '⭐' * int(jsn['data']['feedbacks'][i]['productValuation'])
            markup_list.append(types.InlineKeyboardButton(text=f'{stars} {jsn["data"]["feedbacks"][i]["productDetails"]["supplierArticle"]}', callback_data=f'Review archive info|{jsn["data"]["feedbacks"][i]["id"]}'))
        if len(markup_list) >= 80:
            for i in range(0,80):
                markup_inline.add(markup_list[i])
        else:
            for i in range(len(markup_list)):
                markup_inline.add(markup_list[i])
        four = types.InlineKeyboardButton(text='🔙 Вернуться в отзывы', callback_data='Reviews')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '🗃 Архив отзывов:', reply_markup=markup_inline)

def reviews_archive_info(message, WBToken, x_supplier_id, id):
    jsn = wb_market.GetArchiveReviews(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['data']['feedbacks'])):
            if jsn["data"]["feedbacks"][i]["id"] == id:
                review = jsn["data"]["feedbacks"][i]
        stars = '⭐' * review['productValuation']
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        four = types.InlineKeyboardButton(text='🔙 Вернуться в архив отзывов', callback_data='Reviews Archive')
        markup_inline.add(four)
        bot.send_message(message.chat.id, f'{stars}\nАртикул: {review["productDetails"]["supplierArticle"]}\nНазвание товара: {review["productDetails"]["productName"]}\nОтзыв: {review["text"]}\nОтвет на отзыв: {review["answer"]["text"]}\nДата создания: {review["createdDate"][:10]}', reply_markup=markup_inline)

def new_reviews(message, WBToken, x_supplier_id):
    jsn = wb_market.GetReviews(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        markup_list = []
        if jsn['data']['feedbacks']:
            for i in range(len(jsn['data']['feedbacks'])):
                stars = '⭐' * int(jsn['data']['feedbacks'][i]['productValuation'])
                markup_list.append(types.InlineKeyboardButton(
                    text=f'{stars} {jsn["data"]["feedbacks"][i]["productDetails"]["supplierArticle"]}',
                    callback_data=f'New review menu|{jsn["data"]["feedbacks"][i]["id"]}'))
            if len(markup_list) >= 99:
                for i in range(0, 99):
                    markup_inline.add(markup_list[i])
            else:
                for i in range(len(markup_list)):
                    markup_inline.add(markup_list[i])
        four = types.InlineKeyboardButton(text='🔙 Вернуться в отзывы', callback_data='Reviews')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '📣 Новые отзывы:', reply_markup=markup_inline)

def new_review_menu(message, WBToken, x_supplier_id, id):
    jsn = wb_market.GetReviews(WBToken, x_supplier_id)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        for i in range(len(jsn['data']['feedbacks'])):
            if jsn["data"]["feedbacks"][i]["id"] == id:
                review = jsn["data"]["feedbacks"][i]
        point = int(review['productValuation'])
        stars = '⭐' * point
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        one = types.InlineKeyboardButton(text='✏ Ответить на отзыв', callback_data=f'Review reply|{id}')
        two = types.InlineKeyboardButton(text='📝 Ответить на отзыв по шаблону', callback_data=f'Review reply by sample|{id}|{point}')
        four = types.InlineKeyboardButton(text='🔙 Вернуться в новые отзывы', callback_data='New reviews')
        markup_inline.add(one, two, four)
        bot.send_message(message.chat.id, f'{stars}\nАртикул: {review["productDetails"]["supplierArticle"]}\nНазвание товара: {review["productDetails"]["productName"]}\nОтзыв: {review["text"]}\nДата создания: {review["createdDate"][:10]}', reply_markup=markup_inline)

def patch_to_review(message, WBToken, x_supplier_id, id, text):
    jsn = wb_market.PatchToReview(WBToken, x_supplier_id, id, text)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                         reply_markup=markup_inline)
    else:
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в новые отзывы', callback_data='New reviews')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '✅ Ответ на отзыв успешно опубликован', reply_markup=markup_inline)