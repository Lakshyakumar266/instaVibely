# services/message_service.py
import json

from db.db import get_pool


async def save_message(record):
    pool = await get_pool()

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO incoming_messages (
                instagram_message_id,
                instagram_thread_id,
                sender_id,
                sender_username,
                instagram_user_id,
                message_type,
                status,
                text_content,
                media_id,
                media_url,
                creator_username,
                preview_url,
                audio_id,
                sent_at,
                raw_payload
            )
            VALUES (
                $1,$2,$3,$4,$5,
                $6,$7,$8,$9,$10,
                $11,$12,$13,$14,$15
            )
            ON CONFLICT (instagram_message_id)
            DO NOTHING
            """,
            record["instagram_message_id"],
            record["instagram_thread_id"],
            record["sender_id"],
            record["sender_username"],
            record.get("instagram_user_id"),
            record["message_type"],
            record["status"],
            record["text_content"],
            record["media_id"],
            record["media_url"],
            record["creator_username"],
            record["preview_url"],
            record["audio_id"],
            record["sent_at"],
            json.dumps(record["raw_payload"], default=str),
        )