import pandas as pd 
import yfinance as yf
from models.portfolio import Portfolio
from models.crypto_asset import FetchAPI
from models.crypto_asset import CryptoAsset

class Analytics:
    """
    Analytics class to calculate various metrics about a particular portfolio or assets within 
    that portfolio
    """

    def __init__(self, portfolio:Portfolio, fetch_api=None):
        self.portfolio = portfolio
        self.fetch_api = FetchAPI()

    def get_historical_crypto_data(self, crypto, period):
        asset = self.portfolio.fetch_singular_asset(crypto)
        quantity  = asset[0]['quantity']
        crypto_asset = CryptoAsset(crypto, quantity, self.fetch_api)
        historical_data =  crypto_asset.get_historical_data_period(period)
        return historical_data

    def rolling_mean(self, crypto, window, period):
        crypto_asset = self.get_historical_crypto_data(crypto, period)
        return crypto_asset['Close'].rolling(window=window).mean()

    def moving_volume(self, crypto, window, period):
        crypto_asset = self.get_historical_crypto_data(crypto, period)
        return crypto_asset['Volume'].rolling(window=window).mean()



        



