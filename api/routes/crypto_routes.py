import os
import sys
import uvicorn
from typing import Union, List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.crypto_asset import CryptoAsset, FetchAPI


app = FastAPI()

class AssetInfoResponse(BaseModel): 
    asset: str
    max_supply: Optional[float] = None
    market_cap: Optional[float] = None
    current_price: Optional[float] = None
    total_volume: Optional[float] = None

@app.get("/")
async def root():
    return {"message": "Welcome to the Crypto Portfolio API"}

@app.get("/assets/{asset}/price", response_model=AssetInfoResponse)
async def get_asset_current_price(asset: str):
    crypto_asset = CryptoAsset(asset, FetchAPI())
    current_price = crypto_asset.get_value()
    return AssetInfoResponse(
        asset=asset,
        current_price=current_price
    )

@app.get("/assets/{asset}/max_supply")
async def get_asset_max_supply(asset: str):
    crypto_asset = CryptoAsset(asset, FetchAPI())
    max_supply = crypto_asset.get_max_supply()
    return AssetInfoResponse(
        asset=asset,
        max_supply=max_supply
    )

@app.get("/assets/{asset}/market_cap")
async def get_asset_market_cap(asset: str):
    crypto_asset = CryptoAsset(asset, FetchAPI())
    market_cap = crypto_asset.get_market_cap()
    return AssetInfoResponse(
        asset=asset,
        market_cap=market_cap
    )

@app.get("/assets/{asset}/total_volume")
async def get_asset_total_volume(asset: str):
    crypto_asset = CryptoAsset(asset, FetchAPI())
    total_volume = crypto_asset.get_total_volume()
    return AssetInfoResponse(
        asset=asset,
        total_volume=total_volume
    )

if __name__ == "__main__":
    uvicorn.run("crypto_routes:app", host="127.0.0.1", port=8000, reload=True)