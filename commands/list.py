from services.content_service import (
    get_saved_content
)

def split_message(text: str, max_length: int = 1500):
    chunks = []

    while len(text) > max_length:
        split_at = text.rfind("\n", 0, max_length)

        if split_at == -1:
            split_at = max_length

        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()

    chunks.append(text)

    return chunks

from services.content_service import get_saved_content


def split_message(text: str, max_length: int = 900):
    chunks = []

    while len(text) > max_length:
        split_at = text.rfind("\n", 0, max_length)

        if split_at == -1:
            split_at = max_length

        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()

    chunks.append(text)

    return chunks


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
            reels.append(item)

        elif item["message_type"] == "audio":
            audios.append(item)

        elif item["message_type"] == "post":
            posts.append(item)

    content_lines = []

    for index, item in enumerate(items[:50], start=1):

        emoji = {
            "reel": "🎬",
            "audio": "🎵",
            "post": "📸",
            "text": "📝",
        }.get(item["message_type"], "📦")

        url = item.get("media_url")

        if not url:
            continue

        # Skip broken old records
        if len(url) > 500:
            continue

        content_lines.append(
            f"{index}. {emoji} {url}"
        )

    message = f"""
📚 InstaVibely Library

━━━━━━━━━━━━━━

🎬 Reels: {len(reels)}
🎵 Audio: {len(audios)}
📸 Posts: {len(posts)}

━━━━━━━━━━━━━━

Recent Content

{chr(10).join(content_lines)}

━━━━━━━━━━━━━━

Commands

/list
/hello
/about
"""

    chunks = split_message(
        message.strip(),
        max_length=900,
    )

    for chunk in chunks:
        print("=" * 80)
        print("SENDING CHUNK")
        print(f"Length: {len(chunk)}")
        print(chunk)
        print("=" * 80)
        await client.direct_send(text=chunk,thread_ids=[str(thread_id)],)