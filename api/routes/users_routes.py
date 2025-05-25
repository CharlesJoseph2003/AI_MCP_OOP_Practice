import os
import sys
import uvicorn
from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add the project root to the Python path when needed
# This approach allows imports to work both when imported as a module and when run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.user import User

app = FastAPI()

class UserResponse(BaseModel): #user response has id because fetch method returns the id 
    id: int
    name: str
    email: str
    age: int

class UserCreate(BaseModel): #create method doesnt use id 
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    param: str
    new_value: Union[int, str]  # This allows either int or str


@app.get("/")
async def root():
    return {"message": "Welcome to the Crypto Portfolio API"}

@app.post("/user/create/", response_model=UserResponse)
async def create_user(user: UserCreate):
    created_user = User.create_user(user.name, user.email, user.age)
    if created_user:
        return UserResponse(
            id=created_user.id,
            name=created_user.name,
            email=created_user.email,
            age=created_user.age
        )
    raise HTTPException(status_code=400, detail="Failed to create user")


@app.get("/user/name/{user_name}", response_model=UserResponse)
async def get_user_by_name(user_name):
    user = User.fetch_user_by_name(user_name)
    if user:
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            age=user.age
        )
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/user/email/{user_email}", response_model=UserResponse)
async def get_user_by_email(user_email):
    user = User.find_user_by_email(user_email)
    if user:
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            age=user.age
        )
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/user/update/name/{user_name}")
async def update_user(user_name: str, user_update: UserUpdate):
    # First fetch the user by name
    user = User.fetch_user_by_name(user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Then call the instance method to update the user
    result = user.update_user(user_update.param, user_update.new_value)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to update user")
    # Update the local user object with the new value
    setattr(user, user_update.param, user_update.new_value)
    # Return the updated user data without fetching again
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        age=user.age
    )

@app.delete("/user/delete/{user_name}")
async def delete_user(user_name: str):
    user = User.fetch_user_by_name(user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    result = user.delete()
    if result:
        return {"message": f"User {user_name} successfully deleted"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete user")


# Run the FastAPI app when this file is executed directly
if __name__ == "__main__":
    uvicorn.run("users_routes:app", host="127.0.0.1", port=8000, reload=True)