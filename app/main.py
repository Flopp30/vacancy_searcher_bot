from fastapi import FastAPI

from bot.settings import POSTGRES_URL
from db import create_async_engine, get_session_maker

app = FastAPI()


def get_session():
    async_engine = create_async_engine(POSTGRES_URL)
    yield await get_session_maker(async_engine)


@app.get('/')
async def home():
    return "Welcome home!"
