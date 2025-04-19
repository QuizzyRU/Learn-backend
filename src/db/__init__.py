from tortoise import Tortoise
from .models.results import Results
from .models.tasks import Tasks
from .models.solution import Solution
from .models.base import Status, Level

async def init_db():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", 
        modules={"models": ["src.db"]},
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()
