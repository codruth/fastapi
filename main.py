from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    description: str = None


@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "message": f"You requested {item_id}"}

@app.post("/items")
def create_item(item: Item):
    return {"message": f"{item.name} has been created"}