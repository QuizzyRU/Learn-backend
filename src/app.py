from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.db import init_db, close_db
from src.routers import admin, tasks, auth, user

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
    allow_headers=["*"],
)

# Mount avatars directory for static file serving
app.mount("/avatars", StaticFiles(directory="avatars"), name="avatars")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(tasks.router, prefix="/task", tags=["Tasks"])
app.include_router(user.router, prefix="/user", tags=["User"])


