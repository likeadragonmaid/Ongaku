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
import re
import sys
import traceback

from ongaku import Config, ongaku
from ongaku.core import filters
from ongaku.core.message import Message
from ongaku.tools import shell, misc


@ongaku.on_message(filters.user_filter)
@ongaku.on_edited_message(filters.user_filter)
async def cmd_dispatcher(ongaku, message):
    message = Message.parse_message(message)
    func = Config.CMD_DICT[message.cmd]
    coro = func(ongaku, message)
    try:
        task = asyncio.Task(coro, name=message.task_id)
        await task
    except asyncio.exceptions.CancelledError:
        await ongaku.log(text=f"<b>#Cancelled</b>:\n<code>{message.text}</code>")
    except BaseException:
        await ongaku.log(
            traceback=str(traceback.format_exc()),
            chat=message.chat.title or message.chat.first_name,
            func=func.__name__,
            name="traceback.txt",
        )


async def worker():
    while True:
        if await get_song() and not Config.LOOP:
            print("Ongaku: Notification not detected.\nOngaku: Bio has been restored to original.")
            await ongaku.set_bio(ongaku.original_bio)
            sys.exit()
        await asyncio.sleep(30)


async def get_song(cmd=False):
    data = await get_data()
    if not data:
        return "Ongaku: No notification detected"
    song = await parse_data(*data)
    if not Config.PLAYLIST or song != Config.PLAYLIST[-1]:
        print("  " + song)
        Config.PLAYLIST.append(song)
        await ongaku.set_bio(bio=song)
        await ongaku.log(text=song)
    if cmd:
        return song


async def get_data():
    rw_data = await shell.run_shell_cmd("termux-notification-list")
    for data in json.loads(rw_data):
        if data["packageName"] == Config.MUSIC_PLAYER:
            return data["title"], data["content"]


async def parse_data(title, content):
    if content == "Tap to see your song history":  # Google Pixel mode
        raw_title = title
    else:
        raw_title = f"""{content + " - " if content else ""}{title}""".replace("_", " ")

    debloated_title = " ".join(
        [word for word in re.split("\W+", raw_title) if word.lower() not in misc.BLOAT]
    )
    val = truncate(debloated_title)
    return val


def truncate(song):
    val = f"▷Now listening: {song}"
    if len(val) > 70:
        val = f"▷{song}"
        if len(val) > 70:
            val = val[0:70:]
    return val
