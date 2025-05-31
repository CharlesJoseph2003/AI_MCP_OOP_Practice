import os
import sys
import uvicorn
import pandas as pd
from typing import Union, List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from services.analytics import Analytics
from models.crypto_asset import FetchAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Crypto Portfolio API"}

@app.get("/analytics/{asset}/rolling_mean")
async def get_rolling_mean(asset: str, window: int, period: str):
    analytics = Analytics(FetchAPI())
    rolling_mean = analytics.rolling_mean(asset, window, period)
    
    # Convert pandas Series to a list of dictionaries with date and value
    # Replace NaN values with None which is JSON serializable
    result = [
        {"date": date.strftime("%Y-%m-%d"), "value": float(value) if not pd.isna(value) else None}
        for date, value in rolling_mean.items()
    ]
    
    return {"asset": asset, "window": window, "period": period, "data": result}

@app.get("/analytics/{asset}/moving_volume")
async def get_moving_volume(asset: str, window: int = Query(..., description="Window size in days"), period: str = Query(..., description="Time period (e.g., '1mo', '1y')")):
    analytics = Analytics(FetchAPI())
    moving_volume = analytics.moving_volume(asset, window, period)
    
    # Convert pandas Series to a list of dictionaries with date and value
    # Replace NaN values with None which is JSON serializable
    result = [
        {"date": date.strftime("%Y-%m-%d"), "value": float(value) if not pd.isna(value) else None}
        for date, value in moving_volume.items()
    ]
    
    return {"asset": asset, "window": window, "period": period, "data": result}

@app.get("/analytics/{asset}/volatility")
async def get_volatility(asset: str, period: str = Query('1y', description="Time period (e.g., '1mo', '1y')"), window: int = Query(30, description="Window size in days")):
    analytics = Analytics(FetchAPI())
    volatility = analytics.calculate_volatility(asset, period, window)
    
    # Convert pandas Series to a list of dictionaries with date and value
    # Replace NaN values with None which is JSON serializable
    result = [
        {"date": date.strftime("%Y-%m-%d"), "value": float(value) if not pd.isna(value) else None}
        for date, value in volatility.items()
    ]
    
    return {"asset": asset, "period": period, "window": window, "data": result}

@app.get("/analytics/{asset}/sharpe_ratio")
async def get_sharpe_ratio(asset: str, risk_free_rate: float = Query(0.02, description="Risk-free rate (default: 2%)"), period: str = Query('1y', description="Time period (e.g., '1mo', '1y')")):
    analytics = Analytics(FetchAPI())
    sharpe_ratio = analytics.calculate_sharpe_ratio(asset, risk_free_rate, period)
    
    # Handle potential NaN values
    sharpe_value = None if pd.isna(sharpe_ratio) else float(sharpe_ratio)
    
    return {"asset": asset, "risk_free_rate": risk_free_rate, "period": period, "sharpe_ratio": sharpe_value}

if __name__ == "__main__":
    uvicorn.run("analytics_routes:app", host="127.0.0.1", port=8000, reload=True)