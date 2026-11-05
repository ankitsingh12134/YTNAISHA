from pyrogram import filters
from pyrogram.types import Message

from ankit import app
from ankit.core.call import Loy
from ankit.utils.database import set_loop
from ankit.utils.decorators import AdminRightsCheck
from ankit.utils.inline import close_markup
from config import BANNED_USERS


@app.on_message(
    filters.command(["end", "stop", "cend", "cstop"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_Music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return
    await Loy.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
