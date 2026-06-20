import asyncio
from client import InstaClient

async def main():
    insta = InstaClient()
    client = await insta.connect()

    threads = await client.direct_threads(amount=1)

    print("SUCCESS")
    print(f"Threads: {len(threads)}")

asyncio.run(main())