def extract_music(media):
    clips = media.get("clips_metadata") or {}

    if clips.get("audio_type") == "licensed_music":
        music = clips.get("music_info")

        if not music:
            return None

        asset = music.get(
            "music_asset_info",
            {}
        )

        return {
            "type": "licensed_music",
            "music_canonical_id": str(
                music.get(
                    "music_canonical_id"
                )
            ),
            "audio_asset_id": str(
                asset.get(
                    "audio_asset_id"
                )
            ),
            "title": asset.get(
                "title"
            ),
            "artist": asset.get(
                "display_artist"
            ),
            "audio_url": asset.get(
                "progressive_download_url"
            ),
            "artwork_url": asset.get(
                "cover_artwork_uri"
            ),
        }

    if clips.get("audio_type") == "original_sounds":
        original = clips.get(
            "original_sound_info"
        )

        return {
            "type": "original_sound",
            "music_canonical_id": str(
                clips.get(
                    "music_canonical_id"
                )
            ),
            "audio_asset_id": str(
                original.get(
                    "audio_asset_id"
                )
            ),
            "title": original.get(
                "original_audio_title"
            ),
            "artist": (
                original
                .get("ig_artist", {})
                .get("username")
            ),
            "audio_url": original.get(
                "progressive_download_url"
            ),
        }

    return None