async def handle_about_command(
    client,
    thread_id,
):
    message = """
ℹ️ About InstaVibely

InstaVibely is a real-time Instagram content collection platform.

It captures content shared through DMs and stores it in a searchable library.

Current Features
✅ Reel Saving
✅ Post Saving
✅ Audio Saving
✅ Text Notes
✅ Content Search (in progress)
✅ AI Processing Pipeline (coming soon)

Vision

Turn Instagram from a content feed into a personal knowledge base.

Instead of losing great content in bookmarks, chats, and likes, InstaVibely helps you collect, organize, search, and eventually analyze everything you discover.

Built with:
• Python
• aiograpi MQTT
• Neon PostgreSQL
• AI Workflows

Version: v1

"""

    await client.direct_send(
        text=message.strip(),
        thread_ids=[str(thread_id)],
    )