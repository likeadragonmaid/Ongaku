import asyncio
import os
import sys
from subprocess import run

from ongaku.looper import get_song, reset_bio
from pyrogram import filters
from pyrogram.types import Message

from ongaku import current_, git_branch
from ongaku import ongaku as ong
from ongaku import trigger, users

from .neofetch import neofetch

Repos = "https://github.com/Ongaku-TG/ongaku"


@ong.on_message(
    filters.command(commands="about", prefixes=trigger) & filters.user(users), group=4
)
async def about_(ong, message: Message):
    await message.delete()
    about = f"A **smol and fluffy** telegram bot to update your bio with music playing on your android phone in real time!\n\n[Get it now!]({Repos})"
    return await message.reply(about, disable_web_page_preview=True)


@ong.on_message(
    filters.command(commands="sync", prefixes=trigger) & filters.user(users), group=1
)
async def sync_(ong, message: Message):
    await message.delete()
    check_song = await get_song(check=True)
    await message.reply(check_song)


@ong.on_message(
    filters.command(commands="history", prefixes=trigger) & filters.user(users), group=4
)
async def history_(ong, message: Message):
    await message.delete()
    history = "\n".join(
        [f"**{indx+1}**. __{val}__" for indx, val in enumerate(current_[1:])]
    )
    if not history:
        history = "Ongaku: Nothing has been played in the current session"
    await message.reply(history)


@ong.on_message(
    filters.command(commands="alive", prefixes=trigger) & filters.user(users), group=5
)
async def neo_alive(ong, message: Message):
    await message.delete()
    out_msg = await message.reply("`Ongaku: Please wait...`")
    rw_msg = message.text.split()
    neo = run("neofetch --stdout", shell=True, capture_output=True).stdout.decode(
        "utf-8"
    )
    if not neo:
        return await out_msg.edit("Ongaku: Neofetch is not installed\nTip: Check README.md")
    if "-t" in rw_msg:
        return await out_msg.edit(f"`{neo}`")
    neo_gif = await asyncio.to_thread(neofetch, neo)
    if neo_gif == "pil not installed":
        return out_msg.edit("Ongaku: PIL is not installed\nTip: Check README.md")
    caption = f"User : {((await ong.get_me()).mention)}\nGit-Branch : {git_branch}"
    repo = run(
        "git config --get remote.origin.url", shell=True, capture_output=True
    ).stdout.decode("utf-8")
    if repo.strip() != Repos:
        repo_ = "**Unofficial**"
    else:
        repo_ = f"[Link]({repo.strip()})"
    caption += f"Repo : {repo_}"
    await ong.send_document(
        chat_id=message.chat.id, document="neofetch.gif",caption=caption, force_document=True,
    )
    if os.path.isfile("neofetch.gif"):
        os.remove("neofetch.gif")
    await out_msg.delete()


@ong.on_message(
    filters.command(commands="restart", prefixes=trigger) & filters.user(users), group=2
)
async def restart(ong, message: Message):
    await message.delete()
    await reset_bio(restart=True)
    os.system("clear")
    os.execl(sys.executable, sys.executable, "-m", "ongaku")
