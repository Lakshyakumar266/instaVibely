from db.db import get_pool


async def save_song(
    music_canonical_id,
    audio_asset_id,
    title,
    artist,
    spotify_track_id=None,
    spotify_uri=None,
    spotify_url=None,
):
    pool = await get_pool()

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO songs (
                music_canonical_id,
                audio_asset_id,
                title,
                artist,
                spotify_track_id,
                spotify_uri,
                spotify_url
            )
            VALUES (
                $1,$2,$3,$4,$5,$6,$7
            )
            ON CONFLICT (
                music_canonical_id
            )
            DO NOTHING
            """,
            str(music_canonical_id),
            str(audio_asset_id),
            title,
            artist,
            spotify_track_id,
            spotify_uri,
            spotify_url,
        )