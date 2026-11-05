import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from ankit import LOGGER, app, userbot
from ankit.core.call import Loy
from ankit.misc import sudo
from ankit.plugins import ALL_MODULES
from ankit.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        from ankit.utils.database import load_stream_settings

        await load_stream_settings()
    except Exception:
        pass
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("ankit.plugins" + all_module)
    LOGGER("ankit.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Loy.start()
    try:
        await Loy.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ankit").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Loy.decorators()
    LOGGER("ankit").info("ankitBot Started Successfully \n\n Yaha App ko nahi aana hai aapni hf jo bhej sakte hai @Esprosupport ")
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("ankit").info("Stopping Espro Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
