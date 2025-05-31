import os
import sys
import uvicorn
from typing import Union, List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

# Add the project root to the Python path when needed
# This approach allows imports to work both when imported as a module and when run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.portfolio import Portfolio
from models.user import User

# Pydantic models for request/response validation

class AssetCreate(BaseModel): # Contains asset and quantity information
    asset: str
    quantity: float

class AssetResponse(BaseModel): # Contains asset and quantity information
    asset: str
    quantity: float

class PortfolioResponse(BaseModel): # Contains a list of assets in the portfolio
    assets: List[AssetResponse]

class AssetValueResponse(BaseModel): # Used for endpoints that return asset valuation
    asset: str
    value: float
    
class AssetInfoResponse(BaseModel): # Used for endpoints that return asset information
    asset: str
    max_supply: Optional[float] = None
    market_cap: Optional[float] = None

class PortfolioValuationResponse(BaseModel): # Used for total portfolio valuation
    total_value: float
    assets: List[AssetValueResponse]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Crypto Portfolio API"}

def get_user_portfolio(user_name):
    user = User.fetch_user_by_name(user_name)
    portfolio = Portfolio(user)
    return portfolio

# User assets endpoints - RESTful structure
@app.get("/users/{user_name}/assets", response_model=PortfolioResponse)
async def get_user_assets(user_name):
    portfolio = get_user_portfolio(user_name)
    assets_data = portfolio.fetch_user_assets()
    if not assets_data:
        raise HTTPException(status_code=404, detail=f"No assets found for user {user_name}")
    return PortfolioResponse(
        assets=assets_data
    )

@app.get("/users/{user_name}/assets/{asset}", response_model=AssetResponse)
async def get_user_singular_asset(user_name, asset):
    portfolio = get_user_portfolio(user_name)
    asset_data = portfolio.fetch_singular_asset(asset)
    if not asset_data:
        raise HTTPException(status_code=404, detail=f"Asset {asset} not found for user {user_name}")
    return AssetResponse(
        asset=asset_data[0]['asset'],
        quantity=asset_data[0]['quantity']
    )

@app.post("/users/{user_name}/assets", response_model=AssetResponse)
async def add_asset(user_name, asset: AssetCreate):
    portfolio = get_user_portfolio(user_name)
    added_asset = portfolio.add_asset(asset.asset, asset.quantity)
    if not added_asset:
        raise HTTPException(status_code=400, detail=f"Failed to add {asset.asset} to portfolio")
    return AssetResponse(
        asset = added_asset[0]['asset'],
        quantity = added_asset[0]['quantity']
    )

@app.delete("/users/{user_name}/assets/{asset}", response_model=AssetResponse)
async def remove_asset(user_name, asset, quantity: float = Query(..., description="Amount to remove")):
    portfolio = get_user_portfolio(user_name)
    removed_asset = portfolio.remove_asset(asset, quantity)
    if not removed_asset:
        raise HTTPException(status_code=400, detail=f"Failed to remove {asset} from portfolio")
    return AssetResponse(
        asset = removed_asset[0]['asset'],
        quantity = removed_asset[0]['quantity']
    )

@app.get("/users/{user_name}/valuation", response_model=PortfolioValuationResponse)
async def get_total_portfolio_valuation(user_name):
    portfolio = get_user_portfolio(user_name)
    total_value = portfolio.total_portfolio_valuation()
    
    # Get individual asset values for the response
    assets_data = portfolio.fetch_user_assets()
    asset_values = []
    for asset_data in assets_data:
        asset_symbol = asset_data['asset']
        asset_value = portfolio.crypto_current_price(asset_symbol)
        asset_values.append(AssetValueResponse(
            asset=asset_symbol,
            value=asset_value
        ))
    
    return PortfolioValuationResponse(
        total_value=total_value,
        assets=asset_values
    )

@app.get("/users/{user_name}/assets/{asset}/value", response_model=AssetValueResponse)
async def get_asset_total_value(user_name, asset):
    portfolio = get_user_portfolio(user_name)
    value = portfolio.crypto_current_price(asset)
    return AssetValueResponse(
        asset=asset,
        value=value
    )

if __name__ == "__main__":
    uvicorn.run("portfolio_routes:app", host="127.0.0.1", port=8000, reload=True)