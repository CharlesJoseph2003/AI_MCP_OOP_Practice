from models.crypto_asset import CryptoAsset, FetchAPI
from models.user import User
from repositories.portfolio_repository import PortfolioRepository

class Portfolio:
    """Portfolio class for managing user cryptocurrency portfolios.
    
    This class provides methods for adding, removing, and querying assets in a user's portfolio,
    as well as calculating portfolio valuations and individual asset values.
    """
    def __init__(self, user: User, fetch_api=None):
        """Initialize a Portfolio instance for a specific user.
        
        Args:
            user (User): User object containing user information (id, name)
            fetch_api (FetchAPI, optional): API for fetching cryptocurrency data. Defaults to None.
        """
        self.user_id = user.id
        self.name = user.name
        self.fetch_api = FetchAPI()

    def fetch_user_assets(self):
        """Retrieve all cryptocurrency assets owned by the user.
        
        Returns:
            list: List of dictionaries containing asset information (asset symbol and quantity)
        """
        return PortfolioRepository.fetch_user_assets(self.user_id)
            
    def fetch_singular_asset(self, asset):
        """Retrieve information about a specific asset in the user's portfolio.
        
        Args:
            asset (str): Symbol of the cryptocurrency asset to retrieve
            
        Returns:
            list: List containing a dictionary with asset information
        """
        return PortfolioRepository.fetch_asset(self.user_id, asset)    

    def get_crypto_data(self, user_asset):
        """Helper function to create a CryptoAsset object for a specific asset.
        
        Args:
            user_asset (str): Symbol of the cryptocurrency asset
            
        Returns:
            CryptoAsset: CryptoAsset object for the specified asset
        """
        crypto = self.fetch_singular_asset(user_asset)
        asset = crypto[0]['asset'],
        clean_asset = asset[0]
        crypto_asset = CryptoAsset(clean_asset, self.fetch_api)
        return crypto_asset

    def check_quantity(self, asset):
        """Check the quantity of a specific asset in the user's portfolio.
        
        Args:
            asset (str): Symbol of the cryptocurrency asset
            
        Returns:
            float: Quantity of the asset owned by the user
        """
        quantity = PortfolioRepository.check_asset_quantity(self.user_id, asset)
        if quantity == 0:
            print(f"No {asset} found for user {self.name}")
        return quantity
    
    def add_quantity(self, asset, new_value):
        """Helper function to calculate the updated quantity after adding or removing assets.
        
        Args:
            asset (str): Symbol of the cryptocurrency asset
            new_value (float): Quantity to add (positive) or remove (negative)
            
        Returns:
            float: Updated total quantity after addition/subtraction
        """
        existing = self.check_quantity(asset)
        updated_value = existing + new_value
        return updated_value

    def add_asset(self, asset, quantity):
        """Add a new asset or update the quantity of an existing asset in the portfolio.
        
        Args:
            asset (str): Symbol of the cryptocurrency asset
            quantity (float): Quantity to add to the portfolio
            
        Returns:
            list: Updated asset information after addition
        """
        updated_value = self.add_quantity(asset, quantity)
        return PortfolioRepository.add_or_update_asset(self.user_id, asset, updated_value)        

    def remove_asset(self, asset, quantity):
        """Remove a specified quantity of an asset from the portfolio.
        
        Args:
            asset (str): Symbol of the cryptocurrency asset
            quantity (float): Quantity to remove from the portfolio
            
        Returns:
            list: Updated asset information after removal
        """
        quantity = -quantity  # Convert to negative for subtraction
        updated_value = self.add_quantity(asset, quantity)
        return PortfolioRepository.add_or_update_asset(self.user_id, asset, updated_value)        
    
    def crypto_current_price(self, user_asset):
        """Calculate the total value of a specific asset in the portfolio.
        
        Args:
            user_asset (str): Symbol of the cryptocurrency asset
            
        Returns:
            float: Total value of the asset based on current price and owned quantity
        """
        crypto_asset = self.get_crypto_data(user_asset)
        quantity = self.check_quantity(user_asset)
        crypto_value = crypto_asset.get_valuation(quantity)
        return crypto_value

    def total_portfolio_valuation(self):
        """Calculate the total value of all assets in the user's portfolio.
        
        Iterates through all assets in the portfolio, calculates their current value,
        and returns the sum of all asset values.
        
        Returns:
            float: Total portfolio value in USD
        """
        total_assets = self.fetch_user_assets()
        total_value = 0
        if not total_assets:
            return 0
        for asset_data in total_assets:
            asset_symbol = asset_data['asset']
            quantity = asset_data['quantity']
            crypto_asset = CryptoAsset(asset_symbol, self.fetch_api)
            asset_value = crypto_asset.get_valuation(quantity)
            total_value += asset_value
        return total_value


# user1 = User('charles', 'charles.joseph2103@gmail.com', 21)
# portfolio = Portfolio(user1)
# print(portfolio.fetch_user_assets())