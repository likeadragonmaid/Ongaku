import os
from subprocess import run

from pyrogram import Client

log_channel = os.environ.get("LOG_CHANNEL")

bio_ = ""

music_player = (
    "com.google.android.as"
    if int(os.environ.get("NOW_PLAYING_PIXEL_MODE", 0))
    else os.environ.get("MUSIC_PLAYER")
)

current_ = ["dummy"]

users = [int(i) for i in os.environ.get("USERS").split(",")]

trigger = os.environ.get("CMD_TRIGGER") or "."

git_branch = run(
    "git branch --show-current", shell=True, capture_output=True
).stdout.decode("utf-8")

operating_system = run("uname -srmo", shell=True, capture_output=True).stdout.decode(
    "utf-8"
)

ongaku = Client(
    name="Ongaku",
    session_string=os.environ.get("STRING_SESSION"),
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
    device_model=("Ongaku"),
    app_version=("git-" + git_branch),
    system_version=(operating_system),
    plugins=dict(root="ongaku.plugins"),
)
