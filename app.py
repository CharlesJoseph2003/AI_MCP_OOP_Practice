from fastapi import FastAPI
import uvicorn
import sys
import os

# Add the current directory to the path so Python can find your modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your route
from api.routes.users_routes import app as users_app

# Create the main app
app = FastAPI()

# Mount your users app
app.mount("/users", users_app)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Crypto Portfolio API"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
