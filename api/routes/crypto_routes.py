import os
import sys
import uvicorn
from typing import Union, List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.crypto_asset import CryptoAsset


app = FastAPI()


@app.get("/{user_name}/portfolio/{asset}/current_price", response_model=AssetValueResponse)
async def get_asset_current_price(user_name, asset):
    portfolio = get_user_portfolio(user_name)
    value = portfolio.crypto_current_price(asset)
    return AssetValueResponse(
        asset=asset,
        value=value
    )

@app.get("/{user_name}/portfolio/{asset}/max_supply", response_model=AssetInfoResponse)
async def get_asset_max_supply(user_name, asset):
    portfolio = get_user_portfolio(user_name)
    max_supply = portfolio.crypto_get_max_supply(asset)
    return AssetInfoResponse(
        asset=asset,
        max_supply=max_supply
    )

@app.get("/{user_name}/portfolio/{asset}/market_cap", response_model=AssetInfoResponse)
async def get_asset_market_cap(user_name, asset):
    portfolio = get_user_portfolio(user_name)
    market_cap = portfolio.crypto_get_marketcap(asset)
    return AssetInfoResponse(
        asset=asset,
        market_cap=market_cap
    )