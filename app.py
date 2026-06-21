import asyncio
import json
from pprint import pprint
from db.db import connect_db 
import socket

from aiograpi.realtime.client import RealtimeClient
from client import InstaClient
from datetime import datetime

from commands.list import handle_list_command
from commands.hello import handle_hello_command
from commands.about import handle_about_command

from commands.reels import handle_reels_command
from commands.posts import handle_posts_command
from commands.audio import handle_audios_command


INSTAGRAM_CLIENT = None

def pretty_print(record):
    print("\n" + "=" * 100)
    print(json.dumps(record, indent=2, default=str))
    print("=" * 100)

def parse_instagram_timestamp(timestamp):
    if not timestamp:
        return None

    try:
        timestamp = int(timestamp)

        # Instagram MQTT timestamps are microseconds
        if timestamp > 9999999999999:
            timestamp /= 1_000_000

        return datetime.fromtimestamp(timestamp)

    except Exception:
        return None

def base_record(msg):
    return {
        "instagram_message_id": str(
            msg.get("message_id")
            or msg.get("item_id")
            or msg.get("id")
        ),

        "instagram_thread_id": str(
            msg.get("thread_id")
        ),

        "sender_id": str(
            msg.get("user_id")
        ),

        "sender_username": None,

        "status": "QUEUE",

        "message_type": "unknown",

        "text_content": None,

        "media_id": None,
        "media_url": None,

        "creator_username": None,

        "audio_id": None,

        "preview_url": None,

        "sent_at": parse_instagram_timestamp(
    msg.get("timestamp")
),

        "raw_payload": msg,
    }


def parse_text(msg):
    record = base_record(msg)

    record.update({
        "message_type": "text",
        "text_content": msg.get("text"),
    })

    return record


def parse_reel(msg):

    reel = msg["xma_clip"][0]

    record = base_record(msg)

    print("\nREEL PAYLOAD")
    print(json.dumps(
        msg["xma_clip"][0],
        indent=2,
        default=str,
    ))

    record.update({
        "message_type": "reel",

        "media_id": str(
            msg.get("original_media_igid")
        ),

        "media_url": reel.get("target_url"),

        "creator_username":
            reel.get("header_title_text"),

        "preview_url":
            reel.get("preview_url"),
    })

    return record


def parse_post(msg):
    post = msg["xma_media_share"][0]

    record = base_record(msg)

    print("\nPOST PAYLOAD")
    print(json.dumps(
        msg["xma_media_share"][0],
        indent=2,
        default=str,
    ))

    record.update({
        "message_type": "post",

        "media_id": str(
            msg.get("original_media_igid")
        ),

        "media_url":
            post.get("target_url"),

        "creator_username":
            post.get("header_title_text"),

        "preview_url":
            post.get("preview_url"),

        "text_content":
            post.get("title_text")
            or post.get("caption_body_text"),
    })

    return record


def parse_audio(msg):
    audio = msg["reels_audio_share"][0]

    audio_id = str(
        msg.get("original_media_igid")
    )

    record = base_record(msg)

    record.update({
        "message_type": "audio",

        "audio_id": audio_id,

        "media_url":
            f"https://www.instagram.com/reels/audio/{audio_id}/",

        "preview_url":
            (
                audio["preview_extra_urls_info"][0]["url"]
                if audio.get("preview_extra_urls_info")
                else None
            ),
    })

    return record


def parse_unknown(msg):
    return base_record(msg)


from services.message_service import save_message

async def save_to_db(record):
    await save_message(record)
    pretty_print(record)

async def send_dm_reply(client,thread_id,text,): 
    await client.direct_send(
        text=text,
        thread_ids=[str(thread_id)],
    )


import traceback
async def process_event(event, client):
    if sender and sender.get("username") == "instavibely.app":
        return

    from services.user_service import resolve_user

    try:
        msg = event["message"]

        sender_id = msg.get("user_id")

        sender = None

        if sender_id:
            sender = await resolve_user(
                client,
                sender_id,
            )

        item_type = msg.get("item_type")

        if item_type == "text":
            text = (msg.get("text") or "").strip().lower()

            if text in ["/list", "list", "/saved"]:
                await handle_list_command(
                    client,
                    msg["thread_id"],
                    sender["instagram_user_id"],
                )
                return

            if text.startswith("/reels"):
                parts = text.split()

                page = 1

                if len(parts) > 1:
                    try:
                        page = int(parts[1])
                    except ValueError:
                        pass

                await handle_reels_command(
                    client,
                    msg["thread_id"],
                    sender["instagram_user_id"],
                    page,
                )
                return

            if text.startswith("/posts"):
                parts = text.split()

                page = 1

                if len(parts) > 1:
                    try:
                        page = int(parts[1])
                    except ValueError:
                        pass

                await handle_posts_command(
                    client,
                    msg["thread_id"],
                    sender["instagram_user_id"],
                    page,
                )
                return

            if text.startswith("/audio"):
                parts = text.split()

                page = 1

                if len(parts) > 1:
                    try:
                        page = int(parts[1])
                    except ValueError:
                        pass

                await handle_audios_command(
                    client,
                    msg["thread_id"],
                    sender["instagram_user_id"],
                    page,
                )
                return

            if text == "/hello":
                await handle_hello_command(
                    client,
                    msg["thread_id"],
                )
                return

            if text == "/about":
                await handle_about_command(
                    client,
                    msg["thread_id"],
                )
                return

            record = parse_text(msg)

        elif item_type == "xma_clip":
            
            record = parse_reel(msg)

        elif item_type == "xma_media_share":
            record = parse_post(msg)

        elif item_type == "reels_audio_share":
            record = parse_audio(msg)

        else:
            record = parse_unknown(msg)

        if sender:
            record["sender_username"] = sender.get("username")
            record["instagram_user_id"] = sender.get(
                "instagram_user_id"
            )

        await save_to_db(record)

    except Exception as e:
        print("❌ PROCESSING ERROR")
        traceback.print_exc()

def on_message(event):
    asyncio.create_task(
        process_event(event, INSTAGRAM_CLIENT)
    )


def on_direct(event):
    pass

async def heartbeat():
    while True:
        print("💓 Alive")
        await asyncio.sleep(300)

async def main():
    await connect_db()

    insta = InstaClient()

    client = await insta.connect()

    global INSTAGRAM_CLIENT
    INSTAGRAM_CLIENT = client
    rt = RealtimeClient(client)

    asyncio.create_task(heartbeat())
    rt.on("message", on_message)
    rt.on("direct", on_direct)

    await rt.connect()

    print("✅ MQTT Connected")

    await rt.direct_subscribe()

    print("✅ Listening for Instagram DMs")

    while True:
        try:
            await rt.read_once()

        except TimeoutError:
            continue

        except socket.timeout:
            continue

        except Exception as e:
            print(f"⚠️ MQTT Connection Lost: {e}")

            while True:
                try:
                    print("🔄 Reconnecting MQTT...")

                    await rt.connect()
                    await rt.direct_subscribe()

                    print("✅ MQTT Reconnected")

                    break

                except Exception as reconnect_error:
                    print(
                        f"❌ Reconnect Failed: "
                        f"{reconnect_error}"
                    )

                    await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())