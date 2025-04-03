import asyncio
from .server import Server

# Registration functions
def register(block=False):
    Server.init()
    Server.run()
    if block:
        asyncio.get_event_loop().run_forever()  # 阻塞当前线程

def unregister():
    pass