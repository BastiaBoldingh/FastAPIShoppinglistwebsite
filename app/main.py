from app.core.database import Base, engine
from fastapi import FastAPI
from app.api.v1.auth import router as auth_router



Base.metadata.create_all(bind=engine)


app = FastAPI(title="Shopping List API", version="1.0")

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Shopping List API!"}





