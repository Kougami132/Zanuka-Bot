from nonebot import get_bot, on_regex, on_command, require
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from datetime import datetime, timedelta
from ..util import get_config, set_config, count_down
from ..worldstate.query import queryWorldstate


groups = get_config("monitor", "default", "groups").split(',') if get_config("monitor", "default", "groups") else []
keywords = get_config("monitor", "keywords", "all").split(',') if get_config("monitor", "keywords", "all") else []
scheduler = require('nonebot_plugin_apscheduler').scheduler
enable_monitor = on_regex(r"^开启监控$", permission=SUPERUSER)
disable_monitor = on_regex(r"^关闭监控$", permission=SUPERUSER)
add_monitor = on_command("添加监控", permission=SUPERUSER)
del_monitor = on_command("删除监控", permission=SUPERUSER)


@enable_monitor.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global groups
    group = str(event.group_id)
    if group in groups:
        await bot.send(event, "本群已在监控通知列表,请勿重复操作")
    else:
        groups.append(group)
        set_config("monitor", "default", "groups", ",".join(groups))
        await bot.send(event, "成功将本群添加到监控通知列表")

@disable_monitor.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    global groups
    group = str(event.group_id)
    if group in groups:
        groups.remove(group)
        set_config("monitor", "default", "groups", ",".join(groups))
        await bot.send(event, "成功将本群移除监控通知列表")
    else:
        await bot.send(event, "本群不在监控通知列表,无效操作")

@add_monitor.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    global keywords
    keyword = arg.extract_plain_text().strip()
    if keyword in keywords:
        await bot.send(event, f"关键词 [{keyword}] 已在监控列表, 请勿重复操作")
    else:
        keywords.append(keyword)
        set_config("monitor", "keywords", "all", ",".join(keywords))
        await bot.send(event, f"成功将关键词 [{keyword}] 添加到监控列表")

@del_monitor.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    global keywords
    keyword = arg.extract_plain_text().strip()
    if keyword in keywords:
        keywords.remove(keyword)
        set_config("monitor", "keywords", "all", ",".join(keywords))
        await bot.send(event, f"成功将关键词 [{keyword}] 移除监控列表")
    else:
        await bot.send(event, f"关键词 [{keyword}] 不在监控列表,无效操作")


async def send_to_all_groups(content: str):
    global groups
    for i in groups:
        bot = get_bot()
        await bot.send_group_msg(group_id=i, message=content)

@scheduler.scheduled_job('cron', minute='*/10', id='alerts')
async def Alerts_Monitor():
    global keywords
    if not keywords:
        return
    ids = get_config("monitor", "ids", "alerts")
    try:
        data = await queryWorldstate("alerts")
        if not len(data):
            print("[监控:警报]目前无警报")
            return
        flag = False
        for i in data:
            for j in keywords:
                if j.lower() in i["mission"]["reward"]["itemString"].lower():
                    flag = True
                    if i["id"] not in ids:
                        content = f"检测到关键词 [{j}]"
                        content += "\n" + "".center(10, "—")
                        content += f"\n—节点: {i['mission']['node']}"
                        content += f"\n—模式: {i['mission']['type']} ({i['mission']['faction']})"
                        content += f"\n—奖励: {i['mission']['reward']['itemString']}"
                        utcTime = datetime.strptime(i["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
                        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
                        content += "\n—剩余时间: " + count_down(timeLeft)
                        content += "\n" + "".center(10, "—")
                        await send_to_all_groups(content)
                        print(f"[监控:警报]检测到监控关键词[{j}], 已通知到群")
                        ids += i["id"]
                        set_config("monitor", "ids", "alerts", ids)
                    else:
                        print("[监控:警报]检测到已通知数据, 已跳过")
        if ids and not flag:
            set_config("monitor", "ids", "alerts", "")
            print("[监控:警报]未检测到监控关键词")
    except Exception as e:
        print(f"[监控:警报]获取失败 {e}")

@scheduler.scheduled_job('cron', minute='*/10', id='invasions')
async def Invasions_Monitor():
    global keywords
    if not keywords:
        return
    ids = get_config("monitor", "ids", "invasions")
    try:
        data = await queryWorldstate("invasions")
        if not len(data):
            print("[监控:入侵]目前无入侵")
            return
        flag = False
        for i in data:
            if i["completed"]:
                continue
            for j in keywords:
                if len(i["attackerReward"]["countedItems"]) and (j.lower() in i["attackerReward"]["countedItems"][0]["key"].lower() or j.lower() in i["attackerReward"]["countedItems"][0]["type"].lower()) or len(i["defenderReward"]["countedItems"]) and (j.lower() in i["defenderReward"]["countedItems"][0]["key"].lower() or j.lower() in i["defenderReward"]["countedItems"][0]["type"].lower()):
                    flag = True
                    if i["id"] not in ids:
                        content = f"检测到关键词 [{j}]"
                        content += "\n" + "".center(10, "—")
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
                        content += "\n" + "".center(10, "—")
                        await send_to_all_groups(content)
                        print(f"[监控:入侵]检测到监控关键词[{j}], 已通知到群")
                        ids += i["id"]
                        set_config("monitor", "ids", "invasions", ids)
                    else:
                        print("[监控:入侵]检测到已通知数据, 已跳过")
        if ids and not flag:
            set_config("monitor", "ids", "invasions", "")
            print("[监控:入侵]未检测到监控关键词")
    except Exception as e:
        print(f"[监控:入侵]获取失败 {e}")











