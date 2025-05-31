import pandas as pd 
import yfinance as yf
from models.crypto_asset import FetchAPI
from models.crypto_asset import CryptoAsset

class Analytics:
    """
    Analytics class to calculate various metrics about a particular portfolio or assets within 
    that portfolio
    """

    def __init__(self, fetch_api=None):
        """Initialize the Analytics class.
        
        Args:
            fetch_api (FetchAPI, optional): Instance of FetchAPI for cryptocurrency data retrieval.
                If None, a new FetchAPI instance will be created. Defaults to None.
        """
        self.fetch_api = FetchAPI()

    def get_historical_crypto_data(self, crypto, period):
        """Retrieve historical price data for a cryptocurrency over a specified period.
        
        Args:
            crypto (str): Symbol of the cryptocurrency (e.g., 'btc', 'eth')
            period (str): Time period for historical data (e.g., '1d', '1mo', '1y')
            
        Returns:
            pandas.DataFrame: Historical price data including Open, High, Low, Close, and Volume
        """
        crypto_asset = CryptoAsset(crypto, self.fetch_api)
        historical_data =  crypto_asset.get_historical_data_period(period)
        return historical_data

    def rolling_mean(self, crypto, window, period):
        """Calculate the rolling mean (moving average) of closing prices for a cryptocurrency.
        
        Args:
            crypto (str): Symbol of the cryptocurrency (e.g., 'btc', 'eth')
            window (int): Size of the rolling window in days
            period (str): Time period for historical data (e.g., '1mo', '3mo', '1y')
            
        Returns:
            pandas.Series: Rolling mean of closing prices over the specified window
        """
        crypto_asset = self.get_historical_crypto_data(crypto, period)
        return crypto_asset['Close'].rolling(window=window).mean()

    def moving_volume(self, crypto, window, period):
        """Calculate the moving average of trading volume for a cryptocurrency.
        
        Args:
            crypto (str): Symbol of the cryptocurrency (e.g., 'btc', 'eth')
            window (int): Size of the rolling window in days
            period (str): Time period for historical data (e.g., '1mo', '3mo', '1y')
            
        Returns:
            pandas.Series: Rolling mean of trading volume over the specified window
        """
        crypto_asset = self.get_historical_crypto_data(crypto, period)
        return crypto_asset['Volume'].rolling(window=window).mean()

    def calculate_volatility(self, crypto, period='1y', window=30):
        """
        Calculate the volatility (standard deviation of returns) for a cryptocurrency
        
        Args:
            crypto (str): Cryptocurrency symbol
            period (str): Time period for historical data (e.g., '1y', '6mo', '3mo')
            window (int): Rolling window size in days
            
        Returns:
            pandas.Series: Rolling volatility as a percentage
        """
        historical_data = self.get_historical_crypto_data(crypto, period)
        # Calculate daily returns
        returns = historical_data['Close'].pct_change().dropna()
        # Calculate rolling standard deviation and annualize
        volatility = returns.rolling(window=window).std() * (252 ** 0.5) * 100
        return volatility


    def calculate_sharpe_ratio(self, crypto, risk_free_rate=0.02, period='1y'):
        """
        Calculate the Sharpe ratio for a cryptocurrency
        
        Args:
            crypto (str): Cryptocurrency symbol
            risk_free_rate (float): Risk-free rate (default: 2%)
            period (str): Time period for historical data
            
        Returns:
            float: Sharpe ratio
        """
        historical_data = self.get_historical_crypto_data(crypto, period)
        returns = historical_data['Close'].pct_change().dropna()
        
        # Annualized return and volatility
        annual_return = returns.mean() * 252
        annual_volatility = returns.std() * (252 ** 0.5)
        
        # Calculate Sharpe ratio
        sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
        return sharpe_ratio
            



