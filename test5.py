import os
import time
import asyncio
from datetime import datetime


class Game:
    def __init__(self):
        self.run_time = False
        self.time_now = 0
        self.t0 = None
        self.sleep_time = 1
        asyncio.run(self.main())

    async def time_worker(self):
        while True:
            str1 = input()
            if str1 == "d":
                self.run_time = not self.run_time
            else:
                try:
                    self.sleep_time = float(str1)
                except Exception as e:
                    print(e)
            await asyncio.sleep(self.time_now)

    async def time_worker2(self):
        while True:
            if self.run_time:
                self.t0 = time.time()
            if not self.run_time and not self.t0 is None:
                self.time_now = (time.time() - self.t0) / self.sleep_time
                self.t0 = None
                print(self.time_now)
            await asyncio.sleep(self.time_now)

    async def main(self):
        await asyncio.gather(*[self.time_worker(), self.time_worker2()])


if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
m = Game
m()
