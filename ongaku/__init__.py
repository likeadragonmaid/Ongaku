"""

 * __init__.py: Init file for Ongaku

  Copyright (C) 2023 likeadragonmaid, Ryuk

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""

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
