from nonebot.plugin import on_notice, on_message, require
from nonebot.adapters.cqhttp import GroupRecallNoticeEvent, Bot, Message, FriendRecallNoticeEvent, PokeNotifyEvent, \
    MessageEvent, MessageSegment
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent
from nonebot.rule import to_me
from random import choice, randint

poke = on_notice(rule=to_me())
recall = on_notice()
flashimg = on_message()
help = on_message(rule=to_me())

@poke.handle()
async def _(bot: Bot, event: PokeNotifyEvent):
    msg = choice([
        "你再戳！", "？再戳试试？", "别戳了别戳了再戳就坏了555", "我爪巴爪巴，球球别再戳了", "你戳你🐎呢？！",
        "那...那里...那里不能戳...绝对...", "(。´・ω・)ん?", "有事恁叫我，别天天一个劲戳戳戳！", "欸很烦欸！你戳🔨呢",
        "?", "差不多得了😅", "欺负咱这好吗？这不好", "我希望你耗子尾汁"
    ])

    await poke.finish(msg, at_sender=True)

@recall.handle()
async def _(bot: Bot, event: GroupRecallNoticeEvent):
    mid = event.message_id
    meg = await bot.get_msg(message_id=mid)
    if event.user_id != event.self_id and 'type=flash,' not in meg['message']:
        re = 'Killer Queen! 第三の爆弾! Bite The Dust!\n{0}刚刚说了:\n' + meg['message']
        await recall.finish(message=Message(re.format(MessageSegment.at(event.user_id))))

@flashimg.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = str(event.get_message())
    if 'type=flash,' in msg:
        msg = msg.replace('type=flash,', '')
        await flashimg.finish(message=Message("不要发闪照，好东西就要分享。" + msg), at_sender=True)
    else:   #复读
        if not randint(0, 99):
            await flashimg.send(event.get_message())

@help.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    result = "ZANUKA 4.0 https://github.com/Kougami132/ZanukaBot"
    result += "\n信息: 警报 | 入侵 | 裂隙 | 突击 | 仲裁 | 电波 | 特价 | 奸商"
    result += "\n时间: 地球时间 | 平原时间 | 山谷时间 | 幽都时间 | 紫卡时间"
    result += "\n查价: wm | rm"
    result += "\n其他: 涩图(不稳定)"
    result += "\n监控关键词:"
    keywords = require("monitor").keywords
    for i in keywords:
        result += " [{0}]".format(i)
    await help.send(result)
