import fastapi


router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register")
async def register_user():
    pass
        #register a new user

@router.post("/login")
async def login_user():
    pass
        #login a user and return a token

@router.post("/logout")
async def logout_user():
    pass
        #logout a user and invalidate the token

@router.post("/refresh")
async def refresh_token():
    pass
        #refresh the token for a user   
