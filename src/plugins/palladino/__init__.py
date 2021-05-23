from nonebot import on_command
from nonebot.plugin import require
from nonebot.adapters import Bot, Event, Message
from datetime import datetime, timedelta

export = require("tools")
DeltaStr = export.deltastr

palladino = on_command("紫卡时间")

@palladino.handle()
async def _(bot: Bot, event: Event):
    sub = 3 - datetime.now().weekday()
    thursday = datetime.strftime(datetime.now() + timedelta(days=sub), "%Y-%m-%d 08:00:00")
    thurs = datetime.strptime(thursday, '%Y-%m-%d %H:%M:%S')
    if thurs < datetime.now():
        thurs += timedelta(days=7)
    timeLeft = thurs - datetime.now()
    result = "本周Palladino兑换剩余时间: " + DeltaStr(timeLeft)
    await palladino.send(result)
