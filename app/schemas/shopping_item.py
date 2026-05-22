from pydantic import BaseModel
from uuid import UUID



class ShoppingItemAdd(BaseModel): 
    name: str
    quantity: int = 1
    unit: str | None = None
    category_id: UUID | None = None