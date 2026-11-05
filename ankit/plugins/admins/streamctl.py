from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup

from ankit import app
from ankit.misc import SUDOERS, db
from ankit.utils.database import (
    is_autoplay,
    is_nonadmin_chat,
    is_thumb_on,
    set_autoplay,
    set_thumb,
)
from ankit.utils.decorators.language import languageCB
from ankit.utils.formatters import seconds_to_min
from ankit.utils.inline import stream_markup_timer
from ankit.utils.thumbnails import get_thumb
from config import (
    BANNED_USERS,
    SOUNCLOUD_IMG_URL,
    STREAM_IMG_URL,
    TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL,
    adminlist,
)


async def _refresh_markup(message, chat_id, _):
    played, dur = "00:00", "00:00"
    try:
        track = db[chat_id][0]
        played, dur = seconds_to_min(track["played"]), track["dur"]
    except Exception:
        pass
    return InlineKeyboardMarkup(stream_markup_timer(_, chat_id, played, dur))


async def _poster_for(track, chat_id):
    vidid = track.get("vidid")
    try:
        if vidid == "telegram":
            return (
                TELEGRAM_VIDEO_URL
                if track.get("streamtype") == "video"
                else TELEGRAM_AUDIO_URL
            )
        if vidid == "soundcloud":
            return SOUNCLOUD_IMG_URL
        if str(track.get("file", "")).startswith("index_"):
            return STREAM_IMG_URL
        return await get_thumb(vidid)
    except Exception:
        return STREAM_IMG_URL


@app.on_callback_query(filters.regex(r"^StreamSet") & ~BANNED_USERS)
@languageCB
async def stream_settings(client, CallbackQuery, _):
    data = CallbackQuery.data.strip().split(None, 1)[1]
    what, chat = data.split("|")
    chat_id = int(chat)

    # same permission rule as the play/pause buttons
    if not await is_nonadmin_chat(CallbackQuery.message.chat.id):
        if CallbackQuery.from_user.id not in SUDOERS:
            admins = adminlist.get(CallbackQuery.message.chat.id)
            if not admins:
                return await CallbackQuery.answer(_["admin_13"], show_alert=True)
            if CallbackQuery.from_user.id not in admins:
                return await CallbackQuery.answer(_["admin_14"], show_alert=True)

    message = CallbackQuery.message

    if what == "autoplay":
        new = not is_autoplay(chat_id)
        await set_autoplay(chat_id, new)
        await CallbackQuery.answer("Autoplay ON ✅" if new else "Autoplay OFF ❌")
        try:
            await message.edit_reply_markup(await _refresh_markup(message, chat_id, _))
        except Exception:
            pass

    elif what == "thumb":
        new = not is_thumb_on(chat_id)
        await set_thumb(chat_id, new)
        await CallbackQuery.answer("Thumbnail ON" if new else "Thumbnail OFF")
        try:
            track = db[chat_id][0]
        except Exception:
            track = None
        markup = await _refresh_markup(message, chat_id, _)
        try:
            if new:
                # text panel -> photo panel
                text = message.text.html if message.text else ""
                photo = await _poster_for(track or {}, chat_id)
                run = await message.reply_photo(
                    photo=photo, caption=text, reply_markup=markup
                )
            else:
                # photo panel -> text panel
                text = message.caption.html if message.caption else ""
                run = await message.reply_text(
                    text=text, reply_markup=markup, disable_web_page_preview=True
                )
            await message.delete()
            if track is not None:
                track["mystic"] = run
        except Exception:
            try:
                await message.edit_reply_markup(markup)
            except Exception:
                pass
