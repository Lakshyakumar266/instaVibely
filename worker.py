import asyncio
import json
import os
import traceback

from db.db import connect_db
from client import InstaClient

from services.audio_job_service import (
    get_next_job,
    get_next_media,
    mark_processing,
)


DEBUG_DIR = "debug"

os.makedirs(
    DEBUG_DIR,
    exist_ok=True,
)


async def process_job(client, job):
    media_id = job["media_id"]
    media_url = job["media_url"]

    print("=" * 100)
    print("MEDIA ID:", media_id)
    print("MEDIA URL:", media_url)
    print("=" * 100)

    try:
        print("Opening media...")

        media = await client.media_info_v1(
            int(media_id)
        )

        print("SUCCESS")
        print(type(media))

        try:
            dump = media.model_dump()

            with open(
                f"debug/{media_id}.json",
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(
                    dump,
                    f,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )

            print(f"✅ Saved debug/{media_id}.json")

        except Exception:
            traceback.print_exc()

    except Exception as e:
        import traceback
        traceback.print_exc()


async def main():
    await connect_db()

    insta = InstaClient()

    client = await insta.connect()

    print("✅ Worker started")

    while True:
        try:
            job = await get_next_media()

            print("🔍 Looking for jobs...")
            print(job)

            if not job:
                await asyncio.sleep(5)
                continue

            await process_job(
                client,
                job,
            )

        except Exception:
            traceback.print_exc()

            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())