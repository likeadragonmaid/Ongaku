"""

 * main.py: Main logic file of Ongaku

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

from file_extensions import Xtra
from pyrogram import Client, filters
from pyrogram.types import Message

### Global Vars ###

git_branch = run("git branch --show-current", shell=True, capture_output=True).stdout.decode("utf-8")
operating_system = run("uname -srmo", shell=True, capture_output=True).stdout.decode("utf-8")

app = Client(
    name="Ongaku",
    session_string=os.environ.get("STRING_SESSION"),
    api_id=os.environ.get("API_ID"),
    api_hash=os.environ.get("API_HASH"),
    device_model=("Ongaku"),
    app_version=("git-" + git_branch),
    system_version=(operating_system)
)

log_channel = os.environ.get("LOG_CHANNEL")

bio_ = ""

music_player = [os.environ.get("MUSIC_PLAYER")]

looper = os.environ.get("LOOP")

users = os.environ.get("USERS")

users_list = [int(i) for i in users.split(",")]

current_ = ["dummy"]

### Check Loop ###

if looper.lower() == "yes":
    print(
        "\nOngaku: Bot is set to work until manually stopped. It can be stopped by Ctrl+C or killing the process(s)\n"
    )
else:
    print(
        "\nOngaku: Bot is set to stop if there is no music notification. You can change this behavior.\n"
    )

### Ongaku Functions ###


async def main():
    async with app:
        if log_channel:
            await app.send_message(chat_id=int(log_channel), text="Ongaku started")
        print(
            "\nOngaku: Started\nOngaku: Notifications are checked every 30 seconds to avoid spamming the API(s).\nOngaku: Send .sync in any chat to force notification detection."
        )
        me = await app.get_chat("me")
        global bio_
        bio_ = me.bio if me.bio else ""
        while True:
            song = await get_song()
            if song not in ["Ongaku: No notification detected", "Ongaku: Bio update skipped: Notification is stale"] and log_channel:
                await app.send_message(chat_id=int(log_channel), text=song)
            if song == "Ongaku: No notification detected" and looper.lower() != "yes":
                await app.update_profile(bio=bio_)
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
#            title, content = data["title"].strip(Xtra.EXTENTIONS), data[
#                "content"
#            ].strip(Xtra.EXTENTIONS)
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
                await app.update_profile(bio=val)
                current_.append(raw_title)
                print(val)
            else:
                val = "Ongaku: Bio update skipped: Notification is stale"
                #print (val)
    return val


@app.on_message(filters.regex(r"^\.about") & filters.user(users_list))
async def about_(app, message: Message):
    await message.delete()
    about = "A **smol and fluffy** telegram bot to update your bio with music playing on your android phone in real time!\n\n[Get it now!](https://github.com/gibcheesepuffs/ongaku/)"
    return await message.reply(about)


@app.on_message(filters.regex(r"^\.sync") & filters.user(users_list))
async def sync_(app, message: Message):
    await message.delete()
    check_song = await get_song()
    del_ = False
    if check_song == "Ongaku: Bio update skipped: Notification is stale":
        del_ = True
    msg = await message.reply(check_song)
    if del_:
        await asyncio.sleep(10)
        await msg.delete()


@app.on_message(filters.regex(r"^\.history$") & filters.user(users_list))
async def history_(app, message: Message):
    await message.delete()
    history = ""
    count = 0
    for i in current_[1:]:
        count += 1
        history += f"\n**{count}.** `{i}`"
    if not history:
        history = "Ongaku: Nothing has been played in the current session"
    return await message.reply(history)


async def reset_bio():
    print("\n\nOngaku: Resetting bio")
    await app.update_profile(bio=bio_)
    if log_channel:
        return await app.send_message(chat_id=int(log_channel),text="Ongaku: Stopped")


try:
    app.run(main())
except KeyboardInterrupt:
    app.run(reset_bio())
    print("\nOngaku: Stopped")
