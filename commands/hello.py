async def handle_hello_command(
    client,
    thread_id,
):
    message = """
👋 Welcome to InstaVibely

Your personal Instagram content vault.

Simply send me content through DMs and I'll automatically save it for you.

📥 Supported Content
• Reels
• Posts
• Audio / Songs
• Text Notes

✨ What I Do
• Save content automatically
• Organize everything in your private library
• Make content searchable
• Prepare content for future AI workflows

📜 Commands

/hello
Show this welcome message

/about
Learn more about InstaVibely

/list
View your recently saved content

/search <keyword>
Search your saved content
(coming soon)

📝 Examples

Send:
• A Reel
• A Post
• An Audio Track
• A Text Message

I'll save it automatically.

🚀 Built for creators, researchers, students, founders, and anyone who wants a better way to save Instagram content.
"""

    await client.direct_send(
        text=message.strip(),
        thread_ids=[str(thread_id)],
    )