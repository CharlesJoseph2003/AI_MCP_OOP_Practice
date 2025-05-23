import requests
import os
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("CRYPTO_API")
# print(api_key)


class FetchAPI():
    #This is utility class for any coin, it is used to fetch information
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": api_key
        }

    def get_price(self, symbol):
        url = f'{self.base_url}/simple/price/?vs_currencies=usd&symbols={symbol}'
        response = requests.get(url, headers=self.headers)
        return response.json()

    
    def get_coin_market_data(self, symbol):
        url = f'{self.base_url}/coins/markets?vs_currency=usd&symbols={symbol}'
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    
class CryptoAsset:
    def __init__(self, name, quantity, fetch):
        self.fetch = fetch
        self.name = name
        self.quantity = quantity
        self.market_cap = None
        self.initial_price = None
        self.current_price = None
        self.total_volume = None
        self.max_supply = None
        self.valuation = None
        

    def get_metric(self, metric):
        total_data = self.fetch.get_coin_market_data(self.name)
        for data in total_data:
            value = data[metric]
        return value
    
    def get_value(self):
        self.current_price = self.fetch.get_price(self.name)
        return self.current_price[self.name]['usd']

    def get_market_cap(self):
        self.market_cap = self.get_metric('market_cap')
        return self.market_cap

    def get_total_volume(self):
        self.total_volume = self.get_metric("total_volume")
        return self.total_volume
    
    def get_max_supply(self):
        self.max_supply = self.get_metric("max_supply")
        return self.max_supply

    def get_valuation(self):
        self.current_price = self.get_value()
        self.valuation = self.quantity * self.current_price
        return self.valuation
    
    def get_all_data(self):
        historical = yf.Ticker(self.name)
        return historical.info

    def get_historical_data_period(self, period):
        historical = yf.Ticker(self.name, )
        return historical.history(period=period)
        

# fetch = FetchAPI()
# crypto = CryptoAsset('btc', 100, fetch)
# # print(crypto.get_all_data())
# print(crypto.get_historical_data_period('1y'))


    # def get_historical_data():

