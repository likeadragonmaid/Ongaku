"""

 * ongaku.py: Main logic file of Ongaku

  Copyright (C) 2022 Shouko

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

import asyncio
import json
import os
import re
import sys
from subprocess import run

from pyrogram import Client

from .file_extensions import Xtra

""" Global Vars """

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
log_channel = os.environ.get("LOG_CHANNEL")
bio_ = ""
music_player = [os.environ.get("MUSIC_PLAYER")]
looper = os.environ.get("LOOP")
current_ = ["dummy"]
users = [int(i) for i in os.environ.get("USERS").split(",")]
trigger = os.environ.get("CMD_TRIGGER") or "."


""" Check Loop """

if looper.lower() == "yes":
    print(
        "Ongaku: Bot is set to work until manually stopped.\n        It can be stopped by Ctrl+C or killing the process(s)\n"
    )
else:
    print(
        "Ongaku: Bot is set to stop if there is no music notification.\n        You can change this behavior.\n"
    )


async def loop_():
    async with ongaku:
        if log_channel:
            await ongaku.send_message(chat_id=int(log_channel), text="Ongaku started")
        print(
            "Ongaku: Started\nOngaku: Notifications are checked every 30 seconds\n        to avoid spamming the API(s).\nOngaku: Send .sync in any chat to force notification detection.\n\nNow Playing:"
        )
        me = await ongaku.get_chat("me")
        global bio_
        bio_ = me.bio if me.bio else ""
        while True:
            song = await get_song()
            if (
                song
                not in [
                    "Ongaku: No notification detected",
                    "Ongaku: Bio update skipped: Notification is stale",
                ]
                and log_channel
            ):
                await ongaku.send_message(chat_id=int(log_channel), text=song)
            if song == "Ongaku: No notification detected" and looper.lower() != "yes":
                await ongaku.update_profile(bio=bio_)
                print(
                    "Ongaku: Notification not detected.\nOngaku: Bio has been restored to original.\nOngaku: Stopped"
                )
                sys.exit()
                break
            await asyncio.sleep(30)


async def get_song():
    title, content, val = "", "", "Ongaku: No notification detected"
    rw_data = run(
        "termux-notification-list", shell=True, capture_output=True
    ).stdout.decode("utf-8")
    for data in json.loads(rw_data):
        if data["packageName"] in music_player:
            # title, content = data["title"].strip(Xtra.EXTENTIONS), data[
            # "content"
            # ].strip(Xtra.EXTENTIONS)
            title, content = data["title"], data["content"]
            raw_title = f"{content} - {title}".replace("_", " ").strip("- ")
            for i in Xtra.BLOAT:
                remove_bloat = re.compile(re.escape(i), re.IGNORECASE)
                raw_title = remove_bloat.sub("", raw_title)
            remove_space = re.compile(re.escape("  "), re.IGNORECASE)
            raw_title = remove_space.sub("", raw_title)
            full = f"▷Now listening: {raw_title}"
            val = full
            if raw_title != current_[-1]:
                if len(val) > 70:
                    val = f"▷Now listening: {title}"
                    if len(val) > 70:
                        val = f"▷{title}"
                        if len(val) > 70:
                            val = val[0:70:]
                await ongaku.update_profile(bio=val)
                current_.append(raw_title)
                print(f" ▷ {raw_title}")
            else:
                val = "Ongaku: Bio update skipped: Notification is stale"
                # print (val)
    return val


async def reset_bio():
    print("\n\nOngaku: Resetting bio")
    await ongaku.update_profile(bio=bio_)
    if log_channel:
        return await ongaku.send_message(
            chat_id=int(log_channel), text="Ongaku: Stopped"
        )
