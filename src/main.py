import asyncio
import os
import sys


r = sys.path.insert(1, os.path.join(sys.path[0], ".."))

from orm import SyncORM, async_insert_data


state = SyncORM()

if __name__ == "__main__":
    state.select_resume()

