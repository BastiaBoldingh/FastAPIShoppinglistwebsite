from pydantic import BaseModel
from uuid import UUID



class AddCategory(BaseModel): 
    name: str  