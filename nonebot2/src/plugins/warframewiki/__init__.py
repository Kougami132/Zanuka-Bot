from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message
from nonebot.params import CommandArg
from aiocqhttp import ActionFailed
from datetime import datetime, timedelta
from ..util import forward_msg, count_down
from .query import *


wiki = on_command("wiki")




@wiki.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    async def send_error(msg: str):
        await bot.send(event, MessageSegment.reply(event.message_id) + msg)

    try:
        item = arg.extract_plain_text().strip()
        if item == "":
            await send_error("参数不能为空")
            return

        # print(item)

        result = await fetchWiki(item)
        await bot.send(event, result)

    except ActionFailed as e:
        await send_error("账号可能被风控, 请重试!")
    except FileNotFoundError as e:
        await send_error(f"素材丢失: {e}")
    except Exception as e:
        await send_error(f"程序出错：{type(e)}, {e}")
