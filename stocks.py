import requests
import re
import json
import time

currency_symbol = {
    "EUR" : "€",
    "USD" : "$"
}

def currency_conversion(headers, your_currency="EUR"):
        url_currency = f'https://finnhub.io/api/v1/forex/rates?base=USD'
        data = requests.get(url_currency, headers= headers).json()
        conversion = data['quote'][your_currency]
        print(conversion)
        return conversion

def get_stock_symbol(name, headers):
        url_names = f'https://finnhub.io/api/v1/search?q={name}'
        r = requests.get(url_names, headers=headers).json()
        symbol = r['result'][0]['symbol']
        print(info)
        return symbol

def get_stock_price(symbol, headers, your_currency):
        url_prices = f'https://finnhub.io/api/v1/quote?symbol={symbol}'
        res = requests.get(url_prices, headers= headers).json()
        print(res)
        price = res['c'] * currency_conversion(headers, your_currency)
        return price

def exec(msg, user, predicted_cmd):

    cfg = user.get_module_config("finnhub-module")
    your_currency = cfg['currency']
    headers = {'X-Finnhub-Token': cfg['api_token']}
    regex = r".*[von]\s"
    name = re.sub(regex, "", msg)


    if predicted_cmd == "stockprice":
        symbol = get_stock_symbol(name, headers)
        price = get_stock_price(symbol, headers, your_currency)
        return {"cod": 200, "price": price, "msg": f"Die Aktie {name} steht zur Zeit bei einem Kurs von {price:.2f}{currency_symbol[your_currency]}."}

    elif predicted_cmd == "watchlist":
        watchlist_prices = ""
        for i in cfg['watchlist']:
            symbol = i
            print(symbol)
            price = get_stock_price(symbol, headers, your_currency)
            watchlist_prices = f"{watchlist_prices} {symbol}:{price:.2f}{currency_symbol[your_currency]}"
        return {"cod": 200, "msg": f"{watchlist_prices}"}
    else:
        return {"cod":500, "msg": "Ich weiß nicht was du meinst."}