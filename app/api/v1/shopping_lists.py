import fastapi


router = fastapi.APIRouter(prefix="/lists", tags=["shopping_lists"])


@router.get("/")
async def get_shopping_lists():
    pass
        #return all shopping lists for the user 


@router.post("/")
async def create_shopping_list():
    pass
        #create a new shopping list for the user

@router.get("/{list_id}")
async def get_shopping_list(list_id: int): 
    pass
        #return the shopping list with the given id for the user

@router.patch("/{list_id}")
async def update_shopping_list(list_id: int):
    pass
        #update the shopping list with the given id for the user

@router.delete("/{list_id}")
async def delete_shopping_list(list_id: int):
    pass
        #delete the shopping list with the given id for the user