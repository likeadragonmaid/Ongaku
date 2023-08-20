import asyncio
import glob
import importlib
import os
import sys
from functools import wraps
from io import BytesIO

from pyrogram import Client, idle
from pyrogram.enums import ParseMode

from ongaku import Config
from ongaku.core.message import Message


class Ongaku(Client):
    def __init__(self):
        super().__init__(
            name="Ongaku",
            session_string=os.environ.get("STRING_SESSION"),
            api_id=int(os.environ.get("API_ID")),
            api_hash=os.environ.get("API_HASH"),
            in_memory=True,
            parse_mode=ParseMode.DEFAULT,
            sleep_threshold=30,
            max_concurrent_transmissions=2,
            device_model="Ongaku",
            app_version="git-" + Config.GIT_BRANCH,
            system_version=Config.OPERATING_SYSTEM,
        )
        self.original_bio = ""

    def add_cmd(self, cmd, trigger=Config.TRIGGER):  # Custom triggers To do
        def the_decorator(func):
            @wraps(func)
            def wrapper():
                if isinstance(cmd, list):
                    for _cmd in cmd:
                        Config.CMD_DICT[_cmd] = func
                else:
                    Config.CMD_DICT[cmd] = func

            wrapper()
            return func

        return the_decorator

    async def boot(self):
        await super().start()
        await self.import_modules()
        await self.edit_restart_msg()
        await self.log(text="Ongaku started")
        print(
            """Ongaku: Started\nOngaku: Notifications are checked every 30 seconds
        to avoid spamming the API(s).\nOngaku: Send .sync in any chat to force notification detection.\n\nNow Playing:"""
        )
        await self.get_bio()
        from ongaku.Ongaku import worker
        await worker()

    async def edit_restart_msg(self):
        restart_msg = int(os.environ.get("RESTART_MSG", 0))
        restart_chat = int(os.environ.get("RESTART_CHAT", 0))
        if restart_msg and restart_chat:
            await super().get_chat(restart_chat)
            await super().edit_message_text(
                chat_id=restart_chat, message_id=restart_msg, text="Ongaku started."
            )
            os.environ.pop("RESTART_MSG", "")
            os.environ.pop("RESTART_CHAT", "")

    async def get_bio(self):
        me = await self.get_chat("me")
        self.original_bio = me.bio or ""
        if self.original_bio:
            await self.log(text=f"Bio Backup: {self.original_bio}")


    async def import_modules(self):
        for py_module in glob.glob("ongaku/**/*.py"):
            name = os.path.splitext(py_module)[0]
            py_name = name.replace("/", ".")
            importlib.import_module(py_name)

    async def log(
        self,
        text="",
        traceback="",
        chat=None,
        func=None,
        name="log.txt",
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML,
    ):
        if traceback:
            text = f"#Traceback\n<b>Function:</b> {func}\n<b>Chat:</b> {chat}\n<b>Traceback:</b>\n<code>{traceback}</code>"
        return await self.send_message(
            chat_id=Config.LOG_CHAT,
            text=text,
            name=name,
            disable_web_page_preview=disable_web_page_preview,
            parse_mode=parse_mode,
        )

    async def restart(self):
        await self.set_bio(bio=self.original_bio)
        await super().stop(block=False)
        os.execl(sys.executable, sys.executable, "-m", "ongaku")

    async def send_message(self, chat_id, text, name: str = "output.txt", **kwargs):
        if len(str(text)) < 4096:
            return Message.parse_message(
                (await super().send_message(chat_id=chat_id, text=text, **kwargs))
            )
        doc = BytesIO(bytes(text, encoding="utf-8"))
        doc.name = name
        kwargs.pop("disable_web_page_preview", "")
        return await super().send_document(chat_id=chat_id, document=doc, **kwargs)

    async def set_bio(self, bio:str):
        await super().update_profile(bio=bio)