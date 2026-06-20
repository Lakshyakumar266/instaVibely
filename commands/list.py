from services.content_service import (
    get_saved_content
)

async def handle_list_command(
    client,
    thread_id,
):
    items = await get_saved_content()

    if not items:
        await client.direct_send(
            text="""
📭 No saved content found.

Send:
🎬 Reels
🎵 Audio
📸 Posts

and they'll appear here.
""".strip(),
            thread_ids=[str(thread_id)],
        )
        return

    reels = []
    audios = []
    posts = []

    for item in items:
        if item["message_type"] == "reel":
            reels.append(item["media_url"])

        elif item["message_type"] == "audio":
            audios.append(item["media_url"])

        elif item["message_type"] == "post":
            posts.append(item["media_url"])

    message = f"""
📚 InstaVibely Library

━━━━━━━━━━━━━━

🎬 Reels: {len(reels)}
🎵 Audio: {len(audios)}
📸 Posts: {len(posts)}

━━━━━━━━━━━━━━

Recent Content

{chr(10).join(
    f"• {item['media_url']}"
    for item in items[:10]
)}

━━━━━━━━━━━━━━

Commands

/list
/hello
/about
"""

    await client.direct_send(
        text=message.strip(),
        thread_ids=[str(thread_id)],
    )