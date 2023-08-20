import asyncio


async def run_shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
    )
    stdout, _ = await proc.communicate()
    return stdout.decode("utf-8")


class AsyncShell:
    def __init__(self, process):
        self.process = process
        self.full_std = ""
        self.is_done = False

    async def read_output(self):
        while True:
            line = (await self.process.stdout.readline()).decode("utf-8")
            if not line:
                break
            self.full_std += line
        self.is_done = True
        await self.process.wait()

    async def get_output(self):
        while not self.is_done:
            yield self.full_std

    def cancel(self):
        if not self.is_done:
            self.process.kill()
            self._task.cancel()

    @classmethod
    async def run_cmd(cls, cmd, name="shell"):
        sub_process = cls(
            process=await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT
            )
        )
        sub_process._task = asyncio.create_task(
            sub_process.read_output(), name="AsyncShell"
        )
        await asyncio.sleep(0.5)
        return sub_process
