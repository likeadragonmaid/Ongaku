import asyncio
import os
import sys
from subprocess import run

from pyrogram.enums import ChatType

from ongaku import Config, ongaku
from ongaku.Ongaku import get_song
from ongaku.tools.shell import run_shell_cmd

from .neofetch import neofetch

@ongaku.add_cmd(cmd="about")
async def about_(ongaku, message):
    await message.delete()
    repo = (await run_shell_cmd("git config --get remote.origin.url")).strip()
    about = f"A **smol and fluffy** telegram bot to update your bio with music playing on your android phone in real time!\n\n[Get it now!]({repo})"
    return await message.reply(about, disable_web_page_preview=True)


@ongaku.add_cmd(cmd="sync")
async def sync_(ongaku, message):
    await message.delete()
    await message.reply(await get_song(cmd=True))


@ongaku.add_cmd(cmd="history")
async def history_(ongaku, message):
    await message.delete()
    history = "\n".join(
        [f"**{indx+1}**. __{val}__" for indx, val in enumerate(Config.PLAYLIST)]
    )
    if not history:
        history = "Ongaku: Nothing has been played in the current session"
    await message.reply(history)


@ongaku.add_cmd(cmd="alive")
async def neo_alive(ongaku, message):
    reply, _ = await asyncio.gather(message.reply("`Ongaku: Please wait...`"), message.delete())

    neo = await run_shell_cmd("neofetch --stdout")

    if not neo:
        return await out_msg.edit(
            "Ongaku: Neofetch is not installed\nTip: Check README.md"
        )

    if "-t" in message.flags:
        return await reply.edit(f"`{neo}`")

    neo_gif, err = await asyncio.to_thread(neofetch, neo)

    if err:
        return await reply.edit(err)

    caption = f"User : {((await ongaku.get_me()).mention)}\nGit-Branch : {Config.GIT_BRANCH}\n"

    repo = await run_shell_cmd("git config --get remote.origin.url")

    caption += f"Repo : [Link]({repo.strip()})"

    await ongaku.send_document(
        chat_id=message.chat.id,
        document="neofetch.gif",
        caption=caption,
        force_document=True,
    )
    os.remove("neofetch.gif")
    await reply.delete()


@ongaku.add_cmd(cmd="restart")
async def restart(ongaku, message):
    await message.delete()
    reply = await message.reply("restarting....")
    if reply.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        os.environ["RESTART_MSG"] = str(reply.id)
        os.environ["RESTART_CHAT"] = str(reply.chat.id)
    os.system("clear")
    await ongaku.restart()
