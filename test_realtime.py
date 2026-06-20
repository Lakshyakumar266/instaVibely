import asyncio

import os
from pprint import pprint

from aiograpi import Client
from aiograpi.realtime.client import RealtimeClient

SESSION_ID = os.getenv("SESSION_ID")

def on_message(event):
    print("\n" + "=" * 100)
    print("📩 MESSAGE EVENT")
    pprint(event)
    print("=" * 100)


def on_direct(event):
    print("\n" + "=" * 100)
    print("⚡ DIRECT EVENT")
    pprint(event)
    print("=" * 100)


async def main():
    cl = Client()

    await cl.login_by_sessionid(SESSION_ID)

    print("✅ Logged in")

    rt = RealtimeClient(cl)

    rt.on("message", on_message)
    rt.on("direct", on_direct)

    await rt.connect()

    print("✅ MQTT Connected")

    state = await rt.direct_subscribe()

    print("✅ Direct subscribed")
    print(state)

    while True:
        payload = await rt.read_once()

        # optional debug
        # print(payload)

asyncio.run(main())