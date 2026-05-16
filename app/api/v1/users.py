import fastapi

router = fastapi.APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
async def get_current_user():
    pass
        #return the current user


@router.patch("/me")
async def update_current_user():
    pass
        #update the current user    
