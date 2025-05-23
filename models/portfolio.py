from models.crypto_asset import CryptoAsset, FetchAPI
from models.user import User
from repositories.portfolio_repository import PortfolioRepository

class Portfolio:
    def __init__(self, user: User): #passing the User object as a parameter to the class so we can access its attributes like user id and name
        self.user_id = user.id
        self.name = user.name

    def check_quantity(self, asset):
        quantity = PortfolioRepository.check_asset_quantity(self.user_id, asset)
        if quantity == 0:
            print(f"No {asset} found for user {self.name}")
        return quantity
    
    def add_quantity(self, asset, new_value):
        existing = self.check_quantity(asset)
        updated_value = existing + new_value
        return updated_value

    def add_asset(self, asset, quantity):
        updated_value = self.add_quantity(asset, quantity)
        return PortfolioRepository.add_or_update_asset(self.user_id, asset, updated_value)        
    
    def fetch_user_assets(self):
        return PortfolioRepository.fetch_user_assets(self.user_id)
            
    def fetch_singular_asset(self, asset):
        return PortfolioRepository.fetch_asset(asset)    

    def delete_asset(self, asset, quantity):
        quantity = -quantity  # Convert to negative for subtraction
        updated_value = self.add_quantity(asset, quantity)
        return PortfolioRepository.add_or_update_asset(self.user_id, asset, updated_value)        
    
    def crypto_current_price(self, user_asset):
        """Calculate the total value of a singular asset in portfolio"""
        crypto = self.fetch_singular_asset(user_asset)
        asset = crypto[0]['asset'],
        clean_asset = asset[0]
        quantity = crypto[0]['quantity']
  
        fetch_api = FetchAPI()
        crypto_asset = CryptoAsset(clean_asset, quantity, fetch_api)
        crypto_value = crypto_asset.get_valuation()
        return crypto_value


    def total_portfolio_valuation(self):
        """Calculate the total value of all assets in the user's portfolio"""
        total_assets = self.fetch_user_assets()
        total_value = 0
        fetch_api = FetchAPI()
        # Check if we have any assets
        if not total_assets:
            return 0
        # Loop through each asset in the portfolio
        for asset_data in total_assets:
            # Get the asset symbol and quantity
            asset_symbol = asset_data['asset']
            quantity = asset_data['quantity']
            # Create a CryptoAsset object for this asset
            crypto_asset = CryptoAsset(asset_symbol, quantity, fetch_api)
            asset_value = crypto_asset.get_valuation()
            # Add to the total portfolio value
            total_value += asset_value
        return total_value


# user1 = User('charles', 'charles.joseph2103@gmail.com', 21)
# portfolio = Portfolio(user1)
# print(portfolio.crypto_current_price('btc'))