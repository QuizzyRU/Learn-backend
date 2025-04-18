from typer import Typer
from uvicorn import run
from src.app import app as fastapi_app

typer_app = Typer()

@typer_app.command()
def start():
    run(fastapi_app)

if __name__ == "__main__":
    typer_app()

