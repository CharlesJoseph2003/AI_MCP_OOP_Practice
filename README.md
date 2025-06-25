How to clone:
- git clone https://github.com/CharlesJoseph2003/AI_MCP_OOP_Practice.git
- pip install -r requirements.txt




Class Design:

1. CryptoAsset
Represents a single cryptocurrency

Attributes: symbol, name, quantity, initial_price, current_price

Methods: update_price(), get_value(), get_return_percentage()

2. Portfolio
Represents a user's collection of assets

Attributes: user_id, assets: List[CryptoAsset]

Methods: add_asset(), remove_asset(), total_value(), total_return(), update_all_prices()

3. PriceFetcher (API Integration)
Handles external API calls for live crypto prices

Attributes: api_key, base_url

Methods: get_price(symbol), get_bulk_prices(list_of_symbols)

4. AnalyticsEngine
Computes portfolio statistics

Methods: calculate_volatility(asset), average_return(portfolio), sharpe_ratio(portfolio)

5. Alert
Represents an alert for a specific condition

Attributes: symbol, condition_type, threshold, is_triggered

Methods: check_trigger(current_price)

6. AlertManager
Manages multiple alerts

Attributes: alerts: List[Alert]

Methods: add_alert(), remove_alert(), check_all_alerts()

Optional Classes:
7. User
For multi-user support (useful if expanding to web)

Attributes: user_id, email, portfolio: Portfolio

8. CLIInterface / WebInterface
Presents a UI or CLI for user interaction

Technologies Involved:
Python OOP

Public API (e.g. CoinGecko, CoinMarketCap)

Requests or httpx (for API)

Pandas (for analytics)

(Optional) SQLite for persistence

(Optional) Flask/FastAPI for web interface
