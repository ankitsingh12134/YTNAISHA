"""Autoplay: when the queue runs out, queue a related YouTube track."""
import config
from ankit import LOGGER, YouTube
from ankit.misc import db
from ankit.utils.database import is_autoplay
from ankit.utils.stream.queue import put_queue

_history = {}  # chat_id -> recently auto-played video ids


def _is_youtube_track(track):
    vidid = str(track.get("vidid") or "")
    file = str(track.get("file") or "")
    if len(vidid) != 11 or vidid in ("telegram", "soundcloud"):
        return False
    if "live_" in file or "index_" in file:
        return False
    return True


async def autoplay_enqueue(chat_id, last_track) -> bool:
    """Append a related track to db[chat_id]. Returns True if one was queued."""
    try:
        if not is_autoplay(chat_id) or not _is_youtube_track(last_track):
            return False
        hist = _history.setdefault(chat_id, [])
        last_vidid = last_track["vidid"]
        if last_vidid not in hist:
            hist.append(last_vidid)
        pick = None
        for _try in range(4):
            res = await YouTube.autoplay(
                last_vidid,
                last_track["title"],
                max_duration=getattr(config, "DURATION_LIMIT", None),
            )
            if res and res["vidid"] not in hist:
                pick = res
                break
        if not pick:
            return False
        hist.append(pick["vidid"])
        del hist[:-30]
        if chat_id not in db or db[chat_id] is None:
            db[chat_id] = []
        await put_queue(
            chat_id,
            last_track["chat_id"],
            f"vid_{pick['vidid']}",
            pick["title"],
            pick["duration_min"],
            "Autoplay ✨",
            pick["vidid"],
            last_track.get("user_id"),
            last_track.get("streamtype") or "audio",
        )
        return True
    except Exception as e:
        LOGGER(__name__).error(f"Autoplay failed: {e}")
        return False
