import asyncio
import os
from aiograpi import Client

SESSION_ID = os.getenv("SESSION_ID")

async def main():
    client = Client()

    try:
        await client.login_by_sessionid(SESSION_ID)
        print("LOGIN SUCCESS")

    except Exception as e:
        print(type(e).__name__)
        print(e)

asyncio.run(main())