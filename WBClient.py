import requests as r
import json

def GetByKeyword(keyword):
    try:
        rg = r.get(f'https://catalog-ads.wildberries.ru/api/v5/search?keyword={keyword}')
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn

def GetByGood(url):
    url = url.split('/')
    nm = url[4]
    try:
        rg = r.get(f'https://carousel-ads.wildberries.ru/api/v4/carousel?nm={nm}')
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn

def GetByCategory(url):
    url_category = url[26:]
    menuId = 0
    try:
        rg = r.get(f'https://static.wbstatic.net/data/main-menu-ru-ru.json')
        jsn1 = json.loads(rg.text)
    except Exception:
        jsn1 = 'error'
    try:
        pointer = 0
        while pointer != 1:
            for i in range(len(jsn1)):
                if jsn1[i]['url'] == url_category:
                    menuId = int(jsn1[i]['id'])
                    pointer = 1
                elif jsn1[i]['url'] in url_category:
                    jsn1 = jsn1[i]['childs']
                else:
                    menuId = 0
                    break
    except Exception:
        jsn1 = 'error'
    try:
        rg = r.get(f'https://catalog-ads.wildberries.ru/api/v5/catalog?menuid={menuId}')
        jsn = json.loads(rg.text)
    except Exception:
        jsn = 'error'
    return jsn



