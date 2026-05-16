import fastapi


router = fastapi.APIRouter(tags=["shopping_items"])


@router.post("/lists/{list_id}/items")
async def add_shopping_item(list_id: int):
    pass
        #add a new shopping item to the shopping list with the given id for the user


@router.patch("/items/{item_id}")
async def update_shopping_item(item_id: int):
    pass
        #update the shopping item with the given id for the user


@router.delete("/items/{item_id}")
async def delete_shopping_item(item_id: int):
    pass
        #delete the shopping item with the given id for the user

@router.post("/items/reorder")
async def reorder_shopping_items():
    pass
        #reorder the shopping items for the user
    
@router.post("/items/sort")
async def sort_shopping_items():
    pass
        #sort the shopping items for the user

@router.patch("/lists/{list_id}/items/reorder")
async def reorder_shopping_items_in_list(list_id: int):
    pass
        #reorder the shopping items in the shopping list with the given id for the user