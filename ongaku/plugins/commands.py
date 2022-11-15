import asyncio
import os
from subprocess import run

from pyrogram import filters
from pyrogram.types import Message

from ongaku.ongaku import current_, get_song, git_branch, trigger
from ongaku.ongaku import ongaku as ong
from ongaku.ongaku import users

from .neofetch import neofetch

Repos = "https://github.com/Ongaku-TG/ongaku"


@ong.on_message(
    filters.command(commands="about", prefixes=trigger) & filters.user(users), group=4
)
def about_(ong, message: Message):
    message.delete()
    about = f"A **smol and fluffy** telegram bot to update your bio with music playing on your android phone in real time!\n\n[Get it now!]({Repos})"
    return message.reply(about, disable_web_page_preview=True)

@ong.on_message(
    filters.command(commands="sync", prefixes=trigger) & filters.user(users), group=1
)
async def sync_(ong, message: Message):
    await message.delete()
    check_song = await get_song()
    del_ = False
    if check_song == "Ongaku: Bio update skipped: Notification is stale":
        del_ = True
    msg = await message.reply(check_song)
    if del_:
        await asyncio.sleep(10)
        await msg.delete()


@ong.on_message(
    filters.command(commands="history", prefixes=trigger) & filters.user(users), group=4
)
def history_(ong, message: Message):
    message.delete()
    history = ""
    count = 0
    for i in current_[1:]:
        count += 1
        history += f"\n**{count}.** `{i}`"
    if not history:
        history = "Ongaku: Nothing has been played in the current session"
    return message.reply(history)


@ong.on_message(
    filters.command(commands="alive", prefixes=trigger) & filters.user(users), group=5
)
def neo_alive(ong, message: Message):
    message.delete()
    out_msg = message.reply("`Ongaku: Please wait...`")
    rw_msg = message.text.split(" ")
    if "-t" in rw_msg:
        neo = run("neofetch --stdout", shell=True, capture_output=True).stdout.decode(
            "utf-8"
        )
    else:
        neo = neofetch()
    if not neo:
        return out_msg.edit("Ongaku: Neofetch is not installed\nTip: Check README.md")
    if "-t" in rw_msg:
        return out_msg.edit(f"`{neo}`")
    caption = f"User : {(ong.get_me().mention)}\nGit-Branch : {git_branch}"
    repo = run(
        "git config --get remote.origin.url", shell=True, capture_output=True
    ).stdout.decode("utf-8")
    if repo.strip() != Repos: 
        repo_ = "**Unofficial**"
    else:
        repo_= f"[Link]({repo.strip()})"
    caption += f"Repo : {repo_}"
    ong.send_animation(
        chat_id=message.chat.id, animation=neo, caption=caption, unsave=True
    )
    return out_msg.delete()


# @ong.on_message(filters.command(commands="restart", prefixes=trigger) & filters.user(users), group=2)
# async def restart(ong, message: Message):
# to do
