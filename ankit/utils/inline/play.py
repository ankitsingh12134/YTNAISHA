import math
import random
from pyrogram.types import InlineKeyboardButton
from ankit import app
import config
from ankit.utils.formatters import time_to_seconds


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            )
        ],
    ]
    return buttons


def _progress_bar(played_sec, duration_sec, slots=10):
    try:
        ratio = played_sec / duration_sec if duration_sec else 0
    except Exception:
        ratio = 0
    pos = max(0, min(slots - 1, int(ratio * slots)))
    return "━" * pos + "🎵" + "─" * (slots - 1 - pos)


def _safe_seconds(value):
    try:
        return time_to_seconds(value)
    except Exception:
        return 0


def stream_markup_timer(_, chat_id, played, dur):
    from ankit.utils.database import is_autoplay, is_thumb_on

    bar = _progress_bar(_safe_seconds(played), _safe_seconds(dur))
    autoplay = "✅" if is_autoplay(chat_id) else "❌"
    thumb = "ON" if is_thumb_on(chat_id) else "OFF"
    buttons = [
        [
            InlineKeyboardButton(
                text=f"🎶 {played} {bar} {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(text="▶️", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="⏸", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="❄️", callback_data=f"ADMIN Mute|{chat_id}"),
            InlineKeyboardButton(text="⏭", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="🗑", callback_data=f"ADMIN Clear|{chat_id}"),
            InlineKeyboardButton(text="⏹", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(
                text=f"✨ Autoplay {autoplay}",
                callback_data=f"StreamSet autoplay|{chat_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text=f"🖼 THUMBNAIL : {thumb}",
                callback_data=f"StreamSet thumb|{chat_id}",
            )
        ],
        [InlineKeyboardButton(text="❌ CLOSE ❌", callback_data="close")],
    ]
    return buttons


def stream_markup(_, chat_id):
    from ankit.misc import db

    dur = "00:00"
    try:
        dur = db[chat_id][0]["dur"]
    except Exception:
        pass
    return stream_markup_timer(_, chat_id, "00:00", dur)


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"SonaPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"SonaPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons



def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons
            
