#!/usr/local/bin/python3

import argparse
import requests
from expiringdict import ExpiringDict

CACHE = ExpiringDict(max_len = 100, max_age_seconds = 10)

def get(exchange, symbol, param):
    if(exchange == None):
        return None
    elif(exchange.lower() == "bitfinex"):
        return bitfinex(symbol, param)
    elif(exchange.lower() == "koinex"):
        return koinex(symbol, param)    
    else:
        return None

def fetch(url):
    if(url in CACHE):
        return CACHE[url]
    else:
        r = requests.get(url)
        CACHE[url] = r.json()
        return r.json()

def forex(base, to):
    url = "https://api.fixer.io/latest?base=" + base    
    data = fetch(url)
    return float(data["rates"][to.upper()])

def bitfinex(symbol, param):
    url = "https://api.bitfinex.com/v1/pubticker/" + symbol    
    data = fetch(url)
    return float(data[param])

def koinex(symbol, param):
    url = "https://koinex.in/api/ticker"
    data = fetch(url)
    
    if(param == "bid"):
        param = "highest_bid"
    elif(param == "ask"):
        param = "lowest_ask"
  
    info = float(data["stats"][symbol][param])

    return info

def main():
    arg_parser = argparse.ArgumentParser(description = "Crypto currency prices")    
    arg_parser.add_argument("exchange", help = "Exchange name")
    arg_parser.add_argument("symbol", help = "Symbol name")
    arg_parser.add_argument("param", help = "Parameter name")

    args = arg_parser.parse_args()

    print(get(args.exchange, args.symbol, args.param))

if __name__ == "__main__":
    main()

