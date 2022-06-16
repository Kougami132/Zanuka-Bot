from nonebot import on_message
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from ..monitor import keywords


help = on_message(rule=to_me())


@help.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    result = "ZANUKA 5.0"
    result += "\n信息: 警报 | 入侵 | 裂隙 | 突击 | 仲裁 | 电波 | 特价 | 奸商"
    result += "\n时间: 地球时间 | 平原时间 | 山谷时间 | 幽都时间"
    result += "\n查价: wm | rm"
    result += "\n其他: 涩图(不定期开放)"
    result += "\n监控关键词: [" + "] [".join(keywords) + "]" if len(keywords) else "\n监控关键词: 无"
    result += "\nGithub: Kougami132/Zanuka-Bot"
    await bot.send(event, result)

