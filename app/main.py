from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy import text
from database import init_db


# Import routers
from routers import (
    crud,
    )

# Initialize FastAPI
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 'Connected to Postgres via Docker!'"))
    return {"message": result.scalar()}

#include all routers
app.include_router(crud.router)
