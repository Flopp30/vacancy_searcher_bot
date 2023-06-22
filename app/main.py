from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.endpoints.routers import main_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(main_router)
