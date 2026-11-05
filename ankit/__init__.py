from ankit.core.bot import Loy
from ankit.core.dir import dirr
from ankit.core.git import git
from ankit.core.userbot import Userbot
from ankit.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Loy()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
