from services.content_service import (
    get_content_count,
)


async def handle_list_command(
    client,
    thread_id,
    instagram_user_id,
):
    reels = await get_content_count(
    instagram_user_id,
    "reel",)

    posts = await get_content_count(
        instagram_user_id,
        "post",)

    audio = await get_content_count(
        instagram_user_id,
        "audio",)

    text = f"""
📚 InstaVibely Library

━━━━━━━━━━━━━━

🎬 Reels ({reels})
/reels

📸 Posts ({posts})
/posts

🎵 Audio ({audio})
/audio

━━━━━━━━━━━━━━

View content using the commands above.
""".strip()

    await client.direct_send(
        text=text,
        thread_ids=[str(thread_id)],
    )