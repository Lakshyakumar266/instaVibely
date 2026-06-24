from db.db import get_pool


async def create_audio_job(
    media_id,
    media_url,
    instagram_user_id,
):
    pool = await get_pool()

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO audio_jobs (
                media_id,
                media_url,
                instagram_user_id
            )
            VALUES (
                $1,$2,$3
            )
            """,
            media_id,
            media_url,
            instagram_user_id,
        )


async def get_next_job():
    pool = await get_pool()

    async with pool.acquire() as conn:
        return await conn.fetchrow(
            """
            SELECT *
            FROM audio_jobs
            WHERE status = 'PENDING'
            ORDER BY id ASC
            LIMIT 1
            """
        )


async def mark_processing(job_id):
    pool = await get_pool()

    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE audio_jobs
            SET status='PROCESSING'
            WHERE id=$1
            """,
            job_id,
        )
    
async def get_next_media():
    pool = await get_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT *
            FROM incoming_messages
            WHERE message_type IN (
                'reel',
                'post'
            )
            ORDER BY sent_at DESC
            LIMIT 1
            """
        )

    return dict(row) if row else None