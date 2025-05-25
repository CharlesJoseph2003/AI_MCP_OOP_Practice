from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"





# @app.get("/models/{model_name}") #if I visit /models/alexnet, it will return the message below
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}

#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}

#     return {"model_name": model_name, "message": "Have some residuals"}

#Query parameters: key value pairs that are seen in the url which are used to send data to api without changing the path
#ex.
#basic example



# @app.get("/items/")
# def read_item(skip: int = 0, limit: int = 10):
#     return {"skip": skip, "limit": limit}
#if i pass this in the url, http://127.0.0.1:8000/items/?skip=5&limit=20 - fastapi will pass 5 to skip and 10 to limit 
#output looks like this, {"skip":5,"limit":20}
#? question mark indicates the start of a query parameters
#& and seperates multiple parameters

#Can have optional query parameters
# @app.get("/search/")
# def search(q: str = None):
#     return {"query": q}
#url = http://127.0.0.1:8000/search/?q=test
#output = {"query":"test"}



# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: str | None = None, short: bool = False): #item id is a path parameter so it comes before th question mark in the url
#     #the | is not an or operator in this sense, it is just saying that q can either be a string or None. it is Union operator
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


#Request Body
#when need to send data from a client(the browser) to your api, it is sent as a request body
#request body is data sent by the client(browser) to the api
#response body is data api sends to client(browser)

#Pydantic BaseModel is required for FastAPI request bodies because when client sends json to api, the type needs to be validated
#when the browser sends a request to the api, the right format needs to be sent


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# @app.post("/items/")
# async def create_item(item: Item):
#     return item

#can also do request body, with path and query parametrs
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

#response body:{
#   "item_id": 10,
#   "name": "charles",
#   "description": "man",
#   "price": 100,
#   "tax": 10,
#   "q": "hello"
# }