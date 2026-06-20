async def handle_hello_command(
    client,
    thread_id,
):
    message = """
👋 Hello!

Welcome to InstaVibely.

Available Commands:

📚 /list
View saved reels, audio and posts

👋 /hello
Show this message

ℹ️ /about
About InstaVibely
"""

    await client.direct_send(
        text=message.strip(),
        thread_ids=[str(thread_id)],
    )