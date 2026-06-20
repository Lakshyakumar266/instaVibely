import asyncio
import os
from aiograpi import Client

SESSION_ID = os.getenv("SESSION_ID")

client = Client()

async def main():
    await client.login_by_sessionid(
        SESSION_ID
    )

    print("Logged in")

    await client.get_timeline_feed()

    print("Timeline loaded")

    client.dump_settings(
        "session.json"
    )

    print("Session saved")


if __name__ == "__main__":
    asyncio.run(main())