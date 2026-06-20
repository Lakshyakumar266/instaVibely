from db.db import get_pool

async def get_user_by_instagram_id(instagram_user_id):
    pool = await get_pool()

    async with pool.acquire() as conn:
        return await conn.fetchrow(
            """
            SELECT *
            FROM instagram_users
            WHERE instagram_user_id = $1
            """,
            str(instagram_user_id),
        )


async def create_or_update_user(user):
    pool = await get_pool()

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO instagram_users (
                instagram_user_id,
                username,
                full_name,
                profile_pic_url,
                is_verified
            )
            VALUES (
                $1,$2,$3,$4,$5
            )
            ON CONFLICT (instagram_user_id)
            DO UPDATE SET
                username = EXCLUDED.username,
                full_name = EXCLUDED.full_name,
                profile_pic_url = EXCLUDED.profile_pic_url,
                is_verified = EXCLUDED.is_verified,
                updated_at = NOW()
            """,
            str(user["instagram_user_id"]),
            str(user["username"]),
            str(user["full_name"]),
            str(user["profile_pic_url"]),
            bool(user["is_verified"]),
        )

async def resolve_user(client, instagram_user_id):
    existing = await get_user_by_instagram_id(
        instagram_user_id
    )

    if existing:
        return dict(existing)

    user = await client.user_info_v1(
        str(instagram_user_id)
    )

    data = {
        "instagram_user_id": str(user.pk),
        "username": user.username,
        "full_name": user.full_name,
        "profile_pic_url": str(
            getattr(
                user,
                "profile_pic_url",
                ""
            )
        ),
        "is_verified": getattr(
            user,
            "is_verified",
            False,
        ),
    }

    await create_or_update_user(data)

    return data