from nonebot import on_command
import nonebot
from nonebot.adapters.cqhttp.event import Sender
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event, Message
from nonebot.adapters.cqhttp import MessageSegment
import os
import base64

from nonebot import get_driver

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

test = on_command("test")

@test.handle()
async def _(bot: Bot, event: Event, state: T_State):
    print(nonebot.get_bots().copy().popitem()[1])
    print(nonebot.get_bots().copy().popitem()[1])
    # await nonebot.get_bots().popitem()[1].call_api("send_group_msg", **{
    #     "message": "hello world",
    #     "group_id": "1033704948"
    # })
    # await test.send("hello world")
    # try:
        # path = os.path.abspath(os.path.dirname(__file__)) + "\\data\\"
        # file = open(f"{path}miko-daily-023.mp3", "rb")
        # text = base64.b64encode(file.read())
        # file.close()
        # await test.finish(Message(text))
        # await test.finish(Message(f"[CQ:record,url=https://raw.githubusercontent.com/vbup-osc/miko-button/master/static/voices/miko-daily-023.mp3]"))
        # await test.finish(MessageSegment.record("https://raw.githubusercontent.com/vbup-osc/miko-button/master/static/voices/miko-daily-023.mp3"))
        # await test.finish(Message(f"[CQ:record,file=file:///{path}miko-daily-023.mp3]"))
    # with open("./src/plugins/test/data/miko-daily-023.mp3", "rb") as file:
    #     data = base64.b64encode(file.read()).decode()
    #     await test.send(Message(data))
    # except Exception as e:
    #     print(e)
