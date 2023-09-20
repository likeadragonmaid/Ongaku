"""

 * looper.py: Main logic file of Ongaku

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

import asyncio
import json
import os
import re
import sys
from subprocess import run

from ongaku.misc import Xtra

from ongaku import bio_, current_, log_channel, music_player, ongaku

""" Check Loop """
looper = os.environ.get("LOOP")

if looper.lower() == "yes":
    print(
        "Ongaku: Bot is set to work until manually stopped.\n        It can be stopped by Ctrl+C or killing the process(s)\n"
    )
else:
    print(
        "Ongaku: Bot is set to stop if there is no music notification.\n        You can change this behavior.\n"
    )


async def loop_():
    if log_channel:
        await ongaku.send_message(chat_id=int(log_channel), text="Ongaku: Started")
    print(
        "Ongaku: Started\nOngaku: Notifications are checked every 30 seconds\n        to avoid spamming the API(s).\nOngaku: Send .sync in any chat to force notification detection.\n\nNow Playing:"
    )
    me = await ongaku.get_chat("me")
    global bio_
    bio_ = me.bio or ""
    while True:
        song = await get_song(check = False)
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


async def get_song(check : bool=False):
    title, content, val = "", "", "Ongaku: No notification detected"
    rw_data = run(
        "termux-notification-list", shell=True, capture_output=True
    ).stdout.decode("utf-8")
    for data in json.loads(rw_data):
        if data["packageName"] == music_player:
            title, content = data["title"], data["content"]
            
            if (content == "Tap to see your song history"): #Google Pixel mode
                debloated_title = title
                full = f"▷Now listening: {title}"
            else :
                raw_title = f"""{content + " - " if content else ""}{title}""".replace("_", " ")
                debloated_title = " ".join([word for word in re.split("\W+",raw_title) if word.lower() not in Xtra.BLOAT])
                full = f"▷Now listening: {debloated_title}"
            
            val = full
            if debloated_title != current_[-1]:
                if len(val) > 70:
                    val = f"▷Now listening: {debloated_title}"
                    if len(val) > 70:
                        val = f"▷{debloated_title}"
                        if len(val) > 70:
                            val = val[0:70:]
                await ongaku.update_profile(bio=val)
                current_.append(debloated_title)
                print(f"▷ {debloated_title}")
            else:
                val = "Ongaku: Bio update skipped: Notification is stale"
                # print (val)
            if check:
               val = f"▷Now 🎧: __{debloated_title}__"
    return val 


async def reset_bio(restart: bool = False):
    if not restart:
        print("\n\nOngaku: Resetting bio")
        if log_channel:
            await ongaku.send_message(chat_id=int(log_channel), text="Ongaku: Stopped")
    await ongaku.update_profile(bio=bio_)
