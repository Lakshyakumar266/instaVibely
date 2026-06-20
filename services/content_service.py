# services/content_service.py

from db.db import get_pool


async def get_saved_content(limit=50):
    pool = await get_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT
                message_type,
                media_url,
                creator_username,
                sent_at
            FROM incoming_messages
            WHERE message_type IN (
                'reel',
                'audio',
                'post'
            )
            ORDER BY sent_at DESC
            LIMIT $1
            """,
            limit,
        )

    return [dict(row) for row in rows]