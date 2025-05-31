import requests
import os
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("CRYPTO_API")
# print(api_key)


class FetchAPI():
    """Utility class for fetching cryptocurrency data from external APIs.
    
    This class provides methods to interact with the CoinGecko API for retrieving
    various cryptocurrency metrics such as price, market data, and other information.
    """
    def __init__(self):
        """Initialize the FetchAPI with CoinGecko API configuration.
        
        Sets up the base URL and headers required for API requests including the API key.
        """
        self.base_url = "https://api.coingecko.com/api/v3"
        self.headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": api_key
        }

    def get_price(self, symbol):
        """Fetch the current price of a cryptocurrency.
        
        Args:
            symbol (str): Symbol of the cryptocurrency (e.g., 'btc', 'eth')
            
        Returns:
            dict: JSON response containing price data in USD
        """
        url = f'{self.base_url}/simple/price/?vs_currencies=usd&symbols={symbol}'
        response = requests.get(url, headers=self.headers)
        return response.json()

    
    def get_coin_market_data(self, symbol):
        """Fetch comprehensive market data for a cryptocurrency.
        
        Args:
            symbol (str): Symbol of the cryptocurrency (e.g., 'btc', 'eth')
            
        Returns:
            dict: JSON response containing market data including price, market cap, volume, etc.
        """
        url = f'{self.base_url}/coins/markets?vs_currency=usd&symbols={symbol}'
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    
class CryptoAsset:
    """Class representing a cryptocurrency asset with methods to retrieve its metrics.
    
    This class provides an interface to fetch and store various metrics about a cryptocurrency,
    such as price, market cap, volume, and to calculate valuations based on quantity.
    """
    
    def __init__(self, name, fetch):
        """Initialize a CryptoAsset instance.
        
        Args:
            name (str): Symbol of the cryptocurrency (e.g., 'btc', 'eth')
            fetch (FetchAPI): An instance of FetchAPI for making API calls
        """
        self.fetch = fetch
        self.name = name
        self.market_cap = None
        self.initial_price = None
        self.current_price = None
        self.total_volume = None
        self.max_supply = None
        self.valuation = None
        

    def get_info(self):
        """Retrieve general information about the cryptocurrency.
        
        Returns:
            dict: Comprehensive market data for the cryptocurrency
        """
        data = self.fetch.get_coin_market_data(self.name)
        return data

    def get_metric(self, metric):
        """Retrieve a specific metric from the cryptocurrency's market data.
        
        Args:
            metric (str): The name of the metric to retrieve (e.g., 'market_cap', 'total_volume')
            
        Returns:
            float: Value of the requested metric
        """
        total_data = self.fetch.get_coin_market_data(self.name)
        for data in total_data:
            value = data[metric]
        return value
    
    def get_value(self):
        """Retrieve the current price of the cryptocurrency.
        
        Attempts to get the price in USD first, then EUR, and finally falls back to
        the first available currency in the response. Returns 0 if no price is available.
        
        Returns:
            float: Current price of the cryptocurrency
        """
        self.current_price = self.fetch.get_price(self.name)
        # Check which currency is available and use the first one
        if self.name in self.current_price:
            currency_data = self.current_price[self.name]
            # Get the first available currency
            if 'usd' in currency_data:
                return currency_data['usd']
            elif 'eur' in currency_data:
                return currency_data['eur']
            else:
                # Get the first currency in the dictionary
                first_currency = next(iter(currency_data))
                return currency_data[first_currency]
        # If we can't get a price, return 0
        return 0

    def get_market_cap(self):
        """Retrieve the market capitalization of the cryptocurrency.
        
        Returns:
            float: Market capitalization value
        """
        self.market_cap = self.get_metric('market_cap')
        return self.market_cap

    def get_total_volume(self):
        """Retrieve the 24-hour trading volume of the cryptocurrency.
        
        Returns:
            float: Total trading volume
        """
        self.total_volume = self.get_metric("total_volume")
        return self.total_volume
    
    def get_max_supply(self):
        """Retrieve the maximum supply of the cryptocurrency.
        
        Returns:
            float: Maximum supply value, may be None for cryptocurrencies without a fixed supply
        """
        self.max_supply = self.get_metric("max_supply")
        return self.max_supply

    def get_valuation(self, quantity):
        """Calculate the total value of a specified quantity of the cryptocurrency.
        
        Args:
            quantity (float): Amount of the cryptocurrency
            
        Returns:
            float: Total value based on current price and specified quantity
        """
        self.current_price = self.get_value()
        self.valuation = quantity * self.current_price
        return self.valuation
    
    def get_all_data(self):
        """Retrieve comprehensive information about the cryptocurrency from Yahoo Finance.
        
        Returns:
            dict: Detailed information about the cryptocurrency
        """
        historical = yf.Ticker(self.name)
        return historical.info

    def get_historical_data_period(self, period):
        """Retrieve historical price data for the cryptocurrency over a specified period.
        
        Args:
            period (str): Time period for historical data (e.g., '1d', '1mo', '1y')
            
        Returns:
            pandas.DataFrame: Historical price data including Open, High, Low, Close, and Volume
        """
        historical = yf.Ticker(self.name)
        return historical.history(period=period)
        

# fetch = FetchAPI()
# crypto = CryptoAsset('btc', 100, fetch)
# # print(crypto.get_all_data())
# print(crypto.get_historical_data_period('1y'))


    # def get_historical_data():

