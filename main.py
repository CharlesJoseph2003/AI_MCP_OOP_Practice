from models.user import User
from models.portfolio import Portfolio
from models.crypto_asset import FetchAPI
from services.analytics import Analytics

def main():
    # Create users
    user1 = User.fetch_user_by_name('daniel')
    user2 = User.fetch_user_by_name('hannah')
    # user3 = User.create_user('mom', 'mom@gmail.com', 45)
    print(user1.name)
    # user1 = User.update_user_by_name('email', 'daniel@hotmail.com')
     # print(user1)
    # print(User.fetch_all_users())
    # Create portfolios
    portfolio1 = Portfolio(user1)
    portfolio2 = Portfolio(user2)
    # print(portfolio1.fetch_user_assets()) #[{'asset': 'usd', 'quantity': 30}, {'asset': 'btc', 'quantity': 50}, {'asset': 'eth', 'quantity': 40}]
    # print(portfolio1.total_portfolio_valuation()) #5414635.0
    # print(portfolio1.crypto_current_price('btc')) #5,307,900
    # print(portfolio1.crypto_current_price('eth')) #26,585.6
    # print(portfolio1.crypto_current_price('usd')) #367.8
    print(portfolio1.add_asset("btc", 20))


    # print(portfolio1.fetch_singular_asset('btc'))

    fetch_api = FetchAPI()
    analysis = Analytics(portfolio1, fetch_api)
    # print(analysis.rolling_mean('btc', 3, '1mo'))
    
    # Add assets to portfolio
    # print("Adding BTC to portfolio...")
    # result_btc = portfolio1.add_asset('btc', 10)
    # print(f"Result of adding BTC: {result_btc}")
    
    # print("Adding ETH to portfolio...")
    # result_eth = portfolio1.add_asset('eth', 5)
    # print(f"Result of adding ETH: {result_eth}")
    
    # # Get portfolio valuation
    # total_value = portfolio1.total_portfolio_valuation()
    # print(f"Total portfolio value for {user1.name}: ${total_value:.2f}")
    
    # # Get specific asset value
    # btc_value = portfolio1.crypto_current_price('btc')
    # print(f"BTC value for {user1.name}: ${btc_value:.2f}")

if __name__ == "__main__":
    main()
