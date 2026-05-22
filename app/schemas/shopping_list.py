from pydantic import BaseModel

class ShoppingListCreate(BaseModel):
    name: str
    description: str | None = None
    storename: str | None = None

class ShoppingListUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    storename: str | None = None