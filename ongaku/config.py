import json
import os
import platform

from git import Repo


def get_os():
    uname = platform.uname()
    return " ".join((uname.system, uname.release, uname.machine))


class Config:
    CMD_DICT = {}

    GIT_BRANCH = Repo(".").active_branch.name

    DEV_MODE = int(os.environ.get("DEV_MODE", 0))

    LOG_CHAT = int(os.environ.get("LOG_CHANNEL"))

    LOOP = int(os.environ.get("LOOP",0))

    MUSIC_PLAYER = os.environ.get("MUSIC_PLAYER")

    OPERATING_SYSTEM = get_os()

    OWNER_ID = int(os.environ.get("OWNER_ID",0))

    PLAYLIST = []

    TRIGGER = os.environ.get("TRIGGER", ".")

    USERS = json.loads(os.environ.get("USERS", "[]"))
