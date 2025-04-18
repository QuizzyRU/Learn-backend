from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db import init_db, close_db
from src.routers import admin
from src.routers import tasks

async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["GET", "POST"],
)

app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(tasks.router, prefix="/task", tags=["Tasks"])


