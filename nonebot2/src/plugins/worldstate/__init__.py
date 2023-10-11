from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from aiocqhttp import ActionFailed
from datetime import datetime, timedelta
from ..util import forward_msg, count_down
from .query import queryWorldstate


alerts = on_regex(r"^警报(任务)?$")
invasions = on_regex(r"^入侵(任务)?$")
fissures = on_regex(r"^裂隙(任务)?$")
sortie = on_regex(r"^((今|每)日)?突击(任务)?$")
arbitration = on_regex(r"^仲裁(任务)?$")
dailyDeals = on_regex(r"^((今|每)日)?特价(商品)?$")
voidTrader = on_regex(r"^(奸商|虚空商人)(商品)?$")
nightwave = on_regex(r"^电波(任务)?$")
earthCycle = on_regex(r"^地球时间$")
cetusCycle = on_regex(r"^((地球)?((夜灵)?平原)|希图斯)时间$")
vallisCycle = on_regex(r"^((奥布)?山谷|金星平原)(时间|温度|气候)$")
cambionCycle = on_regex(r"^((殁世)?幽都|火卫二平原)时间$")


@alerts.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("alerts")
        if data == []:
            await bot.send(event, MessageSegment.reply(event.message_id) + "没有警报捏")
            return
        nodes = []
        for i in data:
            content = "——————————"
            #节点
            content += f"\n—节点: {i['mission']['node']}"
            #模式
            type = i["mission"]["type"]
            content += f"\n—模式: {type} ({i['mission']['faction']})"
            #奖励
            reward = i["mission"]["reward"]["itemString"]
            content += f"\n—奖励: {reward}"
            #剩余时间
            utcTime = datetime.strptime(i["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
            timeLeft = utcTime + timedelta(hours=8) - datetime.now()
            content += "\n—剩余时间: " + count_down(timeLeft)
            content += "\n——————————"
            nodes.append(content)
        messages = forward_msg(nodes, bot.self_id, "ZANUKA")
        await bot.send_group_forward_msg(group_id=event.group_id, messages=messages)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')

@invasions.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("invasions")
        if data == []:
            await bot.send(event, MessageSegment.reply(event.message_id) + "没有入侵捏")
            return
        nodes = []
        for i in data:
            if i["completed"]:
                continue
            content = "——————————"
            #节点、星球
            content += f"\n—节点: {i['node']}"
            #进攻方进度、派系、奖励
            if len(i["attackerReward"]["countedItems"]):
                content += f"\n—进攻: {round(i['completion'], 1)}% {i['attackerReward']['countedItems'][0]['type']}×{i['attackerReward']['countedItems'][0]['count']}"
            else:
                content += f"\n—进攻: {round(i['completion'], 1)}% 无"
            #防守方进度、派系、奖励
            if len(i["defenderReward"]["countedItems"]):
                content += f"\n—防守: {round(100 - round(i['completion'], 1), 1)}% {i['defenderReward']['countedItems'][0]['type']}×{i['defenderReward']['countedItems'][0]['count']}"
            else:
                content += f"\n—防守: {round(100 - round(i['completion'], 1), 1)}% 无"
            content += "\n——————————"
            nodes.append(content)
        messages = forward_msg(nodes, bot.self_id, "ZANUKA")
        await bot.send_group_forward_msg(group_id=event.group_id, messages=messages)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')

@fissures.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("fissures")
        if data == []:
            await bot.send(event, MessageSegment.reply(event.message_id) + "没有裂隙捏")
            return
        nodes = []

        normal = ["普通裂隙："]
        for tier in range(5):
            content = "————{0}————".format(("古纪", "前纪", "中纪", "后纪", "安魂")[tier])
            for i in data:
                if not i["active"] or i["isStorm"] or i["isHard"]:
                    continue
                if i["tierNum"] == tier + 1:
                    #节点
                    content += f"\n—节点: {i['node']}"
                    #模式
                    content += f"\n—模式: {i['missionType']} ({i['enemy']})"
                    #剩余时间
                    utcTime = datetime.strptime(i["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    timeLeft = utcTime + timedelta(hours=8) - datetime.now()
                    content += "\n—剩余时间: " + count_down(timeLeft)
                    content += "\n——————————"
            normal.append(content)
        nodes.append(normal)

        storm = ["九重天裂隙："]
        for tier in range(5):
            content = "————{0}————".format(("古纪", "前纪", "中纪", "后纪", "安魂")[tier])
            for i in data:
                if not i["active"] or not i["isStorm"]:
                    continue
                if i["tierNum"] == tier + 1:
                    #节点
                    content += f"\n—节点: {i['node']}"
                    #模式
                    content += f"\n—模式: {i['missionType']} ({i['enemy']})"
                    #剩余时间
                    utcTime = datetime.strptime(i["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    timeLeft = utcTime + timedelta(hours=8) - datetime.now()
                    content += "\n—剩余时间: " + count_down(timeLeft)
                    content += "\n——————————"
            storm.append(content)
        nodes.append(storm)

        hard = ["钢铁裂隙："]
        for tier in range(5):
            content = "————{0}————".format(("古纪", "前纪", "中纪", "后纪", "安魂")[tier])
            for i in data:
                if not i["active"] or not i["isHard"]:
                    continue
                if i["tierNum"] == tier + 1:
                    #节点
                    content += f"\n—节点: {i['node']}"
                    #模式
                    content += f"\n—模式: {i['missionType']} ({i['enemy']})"
                    #剩余时间
                    utcTime = datetime.strptime(i["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    timeLeft = utcTime + timedelta(hours=8) - datetime.now()
                    content += "\n—剩余时间: " + count_down(timeLeft)
                    content += "\n——————————"
            hard.append(content)
        nodes.append(hard)

        messages = forward_msg(nodes, bot.self_id, "ZANUKA")
        await bot.send_group_forward_msg(group_id=event.group_id, messages=messages)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')

@sortie.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("sortie")
        result = "今日突击如下:"
        result += "\nBOSS: {0} ({1})".format(data["boss"], data["faction"])
        result += "\n——————————"
        for i in data["variants"]:
            #节点、星球
            result += f"\n—节点: {i['node']}"
            #模式、环境
            result += f"\n—任务: {i['missionType']} ({i['modifier']})"
            result += "\n——————————"
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n—剩余时间: " + count_down(timeLeft)
        await bot.send(event, result)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')

@arbitration.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("arbitration")
        result = "仲裁信息如下:"
        #节点、星球
        result += f"\n节点: {data['node']}"
        #模式、派系
        result += f"\n任务: {data['type']}"
        result += f"\n派系: {data['enemy']}"
        #剩余时间
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n剩余时间: " + count_down(timeLeft)
        await bot.send(event, result)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')

@dailyDeals.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("dailyDeals")
        result = "今日特价商品如下:\n——————————"
        for i in data:
            #商品、价格、数量
            result += f"\n—商品: {i['item']}"
            result += f"\n—价格: {i['salePrice']} ({i['originalPrice']})"
            result += f"\n—数量: {i['total'] - i['sold']}/{i['total']}"
            #剩余时间
            utcTime = datetime.strptime(i["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
            timeLeft = utcTime + timedelta(hours=8) - datetime.now()
            result += "\n—剩余时间: " + count_down(timeLeft)
            result += "\n——————————"
        await bot.send(event, result)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')

@voidTrader.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("voidTrader")
        if not data["active"]:
            content = f"距离 {data['character']} 到达 {data['location']} 中继站还有 "
            utcTime = datetime.strptime(data["activation"], "%Y-%m-%dT%H:%M:%S.%fZ")
            timeLeft = utcTime + timedelta(hours=8) - datetime.now()
            content += count_down(timeLeft)
            await bot.send(event, content)
        else:
            nodes = [f"{data['character']} 已到达 {data['location']} 中继站"]
            content = "——————————————————————————————"
            for i in data["inventory"]:
                content += f"\n—{i['item']}   [{i['ducats']} 杜卡德]   [{i['credits']} 现金]"
            content += "\n——————————————————————————————"
            nodes.append(content)
            messages = forward_msg(nodes, bot.self_id, "ZANUKA")
            await bot.send_group_forward_msg(group_id=event.group_id, messages=messages)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')

@nightwave.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("nightwave")
        nodes = []
        for i in data["activeChallenges"]:
            content = "——————————"
            #任务标题与描述
            content += f"\n—[{i['reputation']}] {i['title']}"
            content += f"\n—任务: {i['desc']}"
            #剩余时间
            utcTime = datetime.strptime(i["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
            timeLeft = utcTime + timedelta(hours=8) - datetime.now()
            content += "\n—剩余时间: " + count_down(timeLeft)
            content += "\n——————————"
            nodes.append(content)
        #本季剩余时间
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        nodes.append(f"本季电波剩余时间: " + count_down(timeLeft))
        messages = forward_msg(nodes, bot.self_id, "ZANUKA")
        await bot.send_group_forward_msg(group_id=event.group_id, messages=messages)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')

@earthCycle.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("earthCycle")
        result = "Zanuka为恁报时:"
        result += "\n地球状态: 白天" if data["isDay"] else "\n地球状态: 夜晚"
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n剩余时间: " + count_down(timeLeft)
        await bot.send(event, result)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')

@cetusCycle.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("cetusCycle")
        result = "Zanuka为恁报时:"
        result += "\n平原状态: 白天" if data["isDay"] else "\n平原状态: 夜晚"
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n剩余时间: " + count_down(timeLeft)
        await bot.send(event, result)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')

@vallisCycle.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("vallisCycle")
        result = "Zanuka为恁报时:"
        result += "\n山谷状态: 温暖" if data["isWarm"] else "\n山谷状态: 寒冷"
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n剩余时间: " + count_down(timeLeft)
        await bot.send(event, result)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')

@cambionCycle.handle()
async def _(bot: Bot, event: MessageEvent):
    try:
        data = await queryWorldstate("cambionCycle")
        result = "Zanuka为恁报时:"
        result += f"\n幽都状态: {str(data['active']).upper()}"
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n剩余时间: " + count_down(timeLeft)
        await bot.send(event, result)
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except FileNotFoundError:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'素材丢失: {e}')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{type(e)}, {e}')
