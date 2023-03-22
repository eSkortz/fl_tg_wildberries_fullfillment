import json
from base64 import b64decode
import requests as r
import time

#ФУНКЦИИ ДЛЯ РАБОТЫ С WILDBERRIES API

#Получение списка новых заказов
def GetOrdersNew(ApiToken):
    try:
        header = {
        'Authorization': f'{ApiToken}',
        }
        rg = r.get(f'https://suppliers-api.wildberries.ru/api/v2/orders?skip=0&take=1000&date_start=2022-01-01T12:30:16Z&status=0', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
#Альтернативный способ получения списка новых заказов без WBAPI
def Alternative_GetOrdersNew(WBToken, x_supplier_id, next):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v3/portal/orders/new?next={next}&order=asc&storeId=all&type=fbs&limit=10', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
def Alternative_GetOrdersNew_1000(WBToken, x_supplier_id, next):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v3/portal/orders/new?next={next}&order=asc&storeId=all&type=fbs&limit=1000', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
def GetOrdersNewCount(WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v3/portal/orders/new/count', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
#Получение списка поставок на сборке
def GetSuppliesInWork(ApiToken):
    try:
        header = {
            'Authorization': f'{ApiToken}',
        }
        rg = r.get(f'https://suppliers-api.wildberries.ru/api/v2/supplies?status=ACTIVE', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
#Альтернативный способ получения списка поставок на сборке без WBAPI
def Alternative_GetSuppliesInWork(WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v3/portal/supplies/assemble?limit=100&next=0&order=asc', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
#Получение списка поставок в доставке
def GetSuppliesOnDelivery(ApiToken):
    try:
        header = {
            'Authorization': f'{ApiToken}',
        }
        rg = r.get(f'https://suppliers-api.wildberries.ru/api/v2/supplies?status=ON_DELIVERY', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
#Альтернативный способ получения списка поставок в доставке без WBAPI
def Alternative_GetSuppliesOnDelivery(WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v3/portal/supplies/delivery?limit=100&next=0&order=asc', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
#Получение pdf файла поставки
def WritePdfBarcode(supply_id, WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v3/portal/supplies/barcode/file?ids={supply_id}', headers=header)
        jsn = json.loads(rg.text)
        pdf64 = jsn['data']['file']
        bytes = b64decode(pdf64, validate=True)
        f = open('barcode.pdf', 'wb')
        f.write(bytes)
        f.close()
        jsn = 'ok'
    except Exception:
        jsn = 'error'
    return jsn
#Получение этикеток поставки
def WritePdfStickers(Orders_list, WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        jsoon = {
            "ids": Orders_list
        }
        rg = r.post(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v3/portal/orders/stickers',
                    headers=header, json=jsoon)
        jsn = json.loads(rg.text)
        pdf64 = jsn['data']['file']
        bytes = b64decode(pdf64, validate=True)
        f = open('stickers.pdf', 'wb')
        f.write(bytes)
        f.close()
        jsn = 'ok'
    except Exception:
        jsn = 'error'
    return jsn
#Получение листа подбора поставки
def WritePdfSelectionSheet(supply_id, Orders_list, WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        jsoon = {
            "ids": Orders_list
        }
        rg = r.post(
            f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v3/portal/supplies/{supply_id}/selection-sheet',
            headers=header, json=jsoon)
        jsn = json.loads(rg.text)
        pdf64 = jsn['data']['file']
        bytes = b64decode(pdf64, validate=True)
        f = open('selection_sheet.pdf', 'wb')
        f.write(bytes)
        f.close()
        jsn = 'ok'
    except Exception:
        jsn = 'error'
    return jsn
#Прикрепление заказов к поставке
def PutOrdersToSupply(ApiToken, supply_id, List):
    try:
        header = {
            'Authorization': f'{ApiToken}',
        }
        jsons = {'orders': List}
        r.put(f'https://suppliers-api.wildberries.ru/api/v2/supplies/{supply_id}', headers=header, json=jsons)
        jsn = 'ok'
    except Exception:
        jsn = 'error'
    return jsn
#Получение списка заказов закрепленных за поставкой
def GetOrdersBySupply(ApiToken, supply_id):
    try:
        header = {
            'Authorization': f'{ApiToken}',
        }
        rg = r.get(f'https://suppliers-api.wildberries.ru/api/v2/supplies/{supply_id}/orders', headers=header)
        jsn = json.loads(rg.text)
        pointer = 0
    except Exception:
        jsn = 'error'
    return jsn
#Закрытие активной поставки
def PostSupplyClose(ApiToken, supply_id):
    try:
        header = {
            'Authorization': f'{ApiToken}',
        }
        r.post(f'https://suppliers-api.wildberries.ru/api/v2/supplies/{supply_id}/close', headers=header)
        jsn = 'ok'
    except Exception:
        jsn = 'error'
    return jsn
#Взятие списка из архива поставок
def GetSuppliesFromArhive(WBToken, x_supplier_id, next, limit):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v3/portal/supplies/complete?limit={limit}&next={next}&order=desc', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
#Создание новой поставки
def PostCreateNewSupply(name, WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        jsoon = {
            'name' : name
        }
        r.post(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v3/portal/supplies', headers=header, json=jsoon)
        jsn = 'ok'
    except Exception:
        jsn = 'error'
    return jsn
#Получить список остатков по товарам
def GetStocks(WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v2/portal/stocks?order=ASC&search=&skip=0&sort=&take=10000', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
#Получить список складов
def GetWarehouses(WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v2/portal/warehouses', headers=header)
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
#Изменить кол-во товара на складе
def PostChangeStocks(barcode, stock, warehouseId, WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        jsoon = {
            'barcode': barcode,
            'stock' : stock,
            'warehouseId' : warehouseId
        }
        r.post(f'https://seller.wildberries.ru/ns/marketplace-app/marketplace-remote-wh/api/v2/portal/stocks', headers=header, json=jsoon)
        jsn = 'ok'
    except Exception:
        jsn = 'error'
    return jsn
#Получение списка новых отзывов
def GetReviews(WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://seller.wildberries.ru/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks?hasSupplierComplaint=&isAnswered=false&metaDataKeyMustNot=norating&nmId=&order=dateDesc&skip=0&take=1000', headers=header)
        rg.encoding = 'UTF-8'
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
#Получение списка архива отзывов
def GetArchiveReviews(WBToken, x_supplier_id):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        rg = r.get(f'https://seller.wildberries.ru/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks?hasSupplierComplaint=&isAnswered=true&metaDataKeyMustNot=norating&nmId=&order=dateDesc&skip=0&take=1000', headers=header)
        rg.encoding = 'UTF-8'
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn
#Опубликовать ответ на отзыв
def PatchToReview(WBToken, x_supplier_id, id, text):
    try:
        header = {
            'Cookie': f"WBToken={WBToken}; x-supplier-id={x_supplier_id}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'
        }
        jsoon = {
            'id' : id,
            'text' : text
        }
        r.patch(f'https://seller.wildberries.ru/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks', headers=header, json=jsoon)
        jsn = 'ok'
    except Exception:
        jsn = 'error'
    return jsn

#END