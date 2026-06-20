async def handle_about_command(
    client,
    thread_id,
):
    message = """
🚀 InstaVibely

Your personal Instagram content vault.

Features:

🎬 Save Reels
🎵 Save Audio
📸 Save Posts
🤖 AI Processing Pipeline
☁️ Neon Database Storage

Built with:
• Python
• aiograpi MQTT
• Neon PostgreSQL

Version: 0.1.0
"""

    await client.direct_send(
        text=message.strip(),
        thread_ids=[str(thread_id)],
    )