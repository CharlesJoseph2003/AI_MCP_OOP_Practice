from models.user import User
from models.portfolio import Portfolio
from models.crypto_asset import CryptoAsset, FetchAPI

def main():
    # Create users
    user1 = User(8, 'daniel', 'daniel@gmail.com', 16)
    user2 = User(12, 'hannah', 'hannah@gmail.com', 20)
    
    # Create portfolios
    portfolio1 = Portfolio(user1)
    portfolio2 = Portfolio(user2)
    
    # Add assets to portfolio
    print("Adding BTC to portfolio...")
    result_btc = portfolio1.add_asset('btc', 10)
    print(f"Result of adding BTC: {result_btc}")
    
    print("Adding ETH to portfolio...")
    result_eth = portfolio1.add_asset('eth', 5)
    print(f"Result of adding ETH: {result_eth}")
    
    # Get portfolio valuation
    total_value = portfolio1.total_portfolio_valuation()
    print(f"Total portfolio value for {user1.name}: ${total_value:.2f}")
    
    # Get specific asset value
    btc_value = portfolio1.crypto_current_price('btc')
    print(f"BTC value for {user1.name}: ${btc_value:.2f}")

if __name__ == "__main__":
    main()
