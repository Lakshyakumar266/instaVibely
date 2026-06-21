from services.content_service import (
    get_content_page,
    get_content_count,
)


async def handle_reels_command(
    client,
    thread_id,
    instagram_user_id,
    page=1,
):
    items = await get_content_page(
    instagram_user_id,
    "reel",
    page,
    5,
)

    total = await get_content_count(
        instagram_user_id,
        "reel"
    )

    if not items:
        await client.direct_send(
            text="📭 No reels found.",
            thread_ids=[str(thread_id)],
        )
        return

    lines = []

    start = ((page - 1) * 5) + 1

    for index, item in enumerate(
        items,
        start=start,
    ):
        creator = (
            item["creator_username"]
            or "Unknown"
        )

        lines.append(
            f"{index}. @{creator}"
        )

    text = f"""
🎬 Saved Reels

Showing {start}-{start + len(items) - 1} of {total}

{chr(10).join(lines)}

━━━━━━━━━━━━━━

Next:
/reels {page + 1}
""".strip()

    await client.direct_send(
        text=text,
        thread_ids=[str(thread_id)],
    )