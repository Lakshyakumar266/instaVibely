import asyncpg
import os

from dotenv import load_dotenv

load_dotenv()

pool = None


async def connect_db():
    global pool

    pool = await asyncpg.create_pool(
        os.getenv("DATABASE_URL"),
        min_size=1,
        max_size=10,
    )

    print("✅ Connected to Neon")


async def get_pool():
    return pool