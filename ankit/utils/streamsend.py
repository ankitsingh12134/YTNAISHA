"""Send the "Started Streaming" panel either with thumbnail or as plain text,
depending on the chat's Thumbnail toggle."""
from ankit import app
from ankit.utils.database import is_thumb_on


def _strip(kw):
    photo = kw.pop("photo", None)
    caption = kw.pop("caption", None)
    return photo, caption


async def send_stream(*args, **kw):
    """Drop-in replacement for app.send_photo(chat_id, photo=, caption=, reply_markup=)."""
    args = list(args)
    chat_id = args.pop(0) if args else kw.pop("chat_id")
    photo, caption = _strip(kw)
    if is_thumb_on(chat_id) and photo:
        return await app.send_photo(chat_id, photo=photo, caption=caption, **kw)
    return await app.send_message(
        chat_id, text=caption, disable_web_page_preview=True, **kw
    )


async def reply_stream(message, *args, **kw):
    """Drop-in replacement for message.reply_photo(photo=, caption=, reply_markup=)."""
    photo, caption = _strip(kw)
    if is_thumb_on(message.chat.id) and photo:
        return await message.reply_photo(photo=photo, caption=caption, **kw)
    return await message.reply_text(
        text=caption, disable_web_page_preview=True, **kw
    )
