from pydantic import BaseModel

class ShoppingListCreate(BaseModel):
    name: str
    description: str | None = None
    storename: str | None = None

