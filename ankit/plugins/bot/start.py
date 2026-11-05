import time

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ChatPermissions,
)
from youtubesearchpython.__future__ import VideosSearch

import config
from ankit import app
from ankit.misc import _boot_
from ankit.plugins.sudo.sudoers import sudoers_list
from ankit.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ankit.utils.decorators.language import LanguageStart
from ankit.utils.formatters import get_readable_time
from ankit.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


# ============================================================
# REQUIRED GROUP
# ============================================================
# Yahan apne group ki ID daalo.
# Example: -1001234567890
#
# IMPORTANT:
# Bot ko is group me Admin hona chahiye aur
# "Restrict Members" permission honi chahiye.
# ============================================================

REQUIRED_START_GROUP_ID = -1003961210499


# ============================================================
# PERMISSIONS
# ============================================================

MUTED_PERMISSIONS = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
)

UNMUTED_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
)


# ============================================================
# PRIVATE START
# ============================================================

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):

    # --------------------------------------------------------
    # START karte hi user ko group me unmute karo
    # --------------------------------------------------------

    try:
        await app.restrict_chat_member(
            chat_id=REQUIRED_START_GROUP_ID,
            user_id=message.from_user.id,
            permissions=UNMUTED_PERMISSIONS,
        )

        await message.reply_text(
            "✅ <b>Verification Complete!</b>\n\n"
            "Ab aap group me message kar sakte ho. 🎉",
        )

    except Exception as e:
        print(f"Start Verification Error: {e}")

    await add_served_user(message.from_user.id)

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        if name[0:4] == "help":
            keyboard = help_pannel(_)

            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )

        if name[0:3] == "sud":
            await sudoers_list(
                client=client,
                message=message,
                _=_,
            )

            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"{message.from_user.mention} "
                        f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                        f"<b>sᴜᴅᴏʟɪsᴛ</b>.\n\n"
                        f"<b>ᴜsᴇʀ ɪᴅ :</b> "
                        f"<code>{message.from_user.id}</code>\n"
                        f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> "
                        f"@{message.from_user.username}"
                    ),
                )

            return

        if name[0:3] == "inf":
            m = await message.reply_text("🔎")

            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"

            results = VideosSearch(query, limit=1)

            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            searched_text = _["start_6"].format(
                title,
                duration,
                views,
                published,
                channellink,
                channel,
                app.mention,
            )

            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=_["S_B_8"],
                            url=link,
                        ),
                        InlineKeyboardButton(
                            text=_["S_B_9"],
                            url=config.SUPPORT_CHAT,
                        ),
                    ],
                ]
            )

            await m.delete()

            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )

            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        f"{message.from_user.mention} "
                        f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ "
                        f"<b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n"
                        f"<b>ᴜsᴇʀ ɪᴅ :</b> "
                        f"<code>{message.from_user.id}</code>\n"
                        f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> "
                        f"@{message.from_user.username}"
                    ),
                )

    else:
        out = private_panel(_)

        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_2"].format(
                message.from_user.mention,
                app.mention,
            ),
            reply_markup=InlineKeyboardMarkup(out),
        )

        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    f"{message.from_user.mention} "
                    f"ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n"
                    f"<b>ᴜsᴇʀ ɪᴅ :</b> "
                    f"<code>{message.from_user.id}</code>\n"
                    f"<b>ᴜsᴇʀɴᴀᴍᴇ :</b> "
                    f"@{message.from_user.username}"
                ),
            )


# ============================================================
# GROUP START
# ============================================================

@app.on_message(
    filters.command(["start"])
    & filters.group
    & ~BANNED_USERS
)
@LanguageStart
async def start_gp(client, message: Message, _):

    out = start_panel(_)

    uptime = int(time.time() - _boot_)

    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(
            app.mention,
            get_readable_time(uptime),
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )

    return await add_served_chat(message.chat.id)


# ============================================================
# NEW MEMBER VERIFICATION
# ============================================================

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):

    for member in message.new_chat_members:

        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            # ------------------------------------------------
            # BANNED USER
            # ------------------------------------------------

            if await is_banned_user(member.id):

                try:
                    await message.chat.ban_member(member.id)
                except Exception:
                    pass

                continue

            # ------------------------------------------------
            # BOT JOINED GROUP
            # ------------------------------------------------

            if member.id == app.id:

                if message.chat.type != ChatType.SUPERGROUP:

                    await message.reply_text(
                        _["start_4"]
                    )

                    return await app.leave_chat(
                        message.chat.id
                    )

                if message.chat.id in await blacklisted_chats():

                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )

                    return await app.leave_chat(
                        message.chat.id
                    )

                out = start_panel(_)

                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )

                await add_served_chat(
                    message.chat.id
                )

                await message.stop_propagation()

                continue

            # ------------------------------------------------
            # NEW USER VERIFICATION
            # ------------------------------------------------

            if message.chat.id == REQUIRED_START_GROUP_ID:

                # New member ko mute karo
                await app.restrict_chat_member(
                    chat_id=message.chat.id,
                    user_id=member.id,
                    permissions=MUTED_PERMISSIONS,
                )

                # Verification message
                await message.reply_text(
                    f"👋 {member.mention}\n\n"
                    "🔒 <b>Group me message karne ke liye "
                    "pehle bot ko START karo.</b>\n\n"
                    "👇 Neeche diye gaye button par click karo "
                    "aur bot ko START karo.\n\n"
                    "✅ START karne ke baad aap group me "
                    "message kar sakte ho.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🤖 START BOT",
                                    url=(
                                        f"https://t.me/"
                                        f"{app.username}"
                                        f"?start=verify"
                                    ),
                                )
                            ]
                        ]
                    ),
                )

        except Exception as ex:
            print(
                f"New Member Verification Error: {ex}"
            )
