from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
root_path = "/" 
if os.getenv("ROUTE"):
    root_path = os.getenv("ROUTE")
app = FastAPI(root_path=root_path)

# In-memory "database"
fake_db = {}

# Request model for POST
class Item(BaseModel):
    name: str
    description: str = None
    price: float

# GET method to retrieve all items
@app.get("/items")
def get_items():
    return fake_db

# GET method to retrieve a specific item by ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id in fake_db:
        return fake_db[item_id]
    raise HTTPException(status_code=404, detail="Item not found")

# POST method to create a new item
@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item_id] = item
    return {"message": "Item created", "item": item}

@app.get("/healthcheck")
def healthcheck():
    return {"Status": "Success"}