from db.db import get_pool


async def get_content_count(instagram_user_id, message_type):
    pool = await get_pool()

    async with pool.acquire() as conn:
        return await conn.fetchval(
            """
            SELECT COUNT(*)
            FROM incoming_messages
            WHERE instagram_user_id = $1
            AND message_type = $2
            """,
            instagram_user_id,
            message_type,
        )

async def get_content_page(
    instagram_user_id,
    message_type,
    page=1,
    per_page=5,
):
    offset = (page - 1) * per_page

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
            WHERE instagram_user_id = $1
            AND message_type = $2
            ORDER BY sent_at DESC
            LIMIT $3
            OFFSET $4
            """,
            instagram_user_id,
            message_type,
            per_page,
            offset,
        )

    return [dict(row) for row in rows]