from datetime import datetime, timedelta
import json
import nonebot
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command, export, require
from nonebot.adapters.cqhttp import Bot, Event, GroupMessageEvent, bot
import os
import configparser
import requests

def Load_Config():
    global groups, keywords, cp, ex
    groups = cp.get("monitor", "groups").split(",")
    groups = [i for i in groups if i != ""]
    keywords = cp.get("monitor", "keywords").split(",")
    keywords = [i for i in keywords if i != ""]
    ex.groups = groups
    ex.keywords = keywords

def Save_Config():
    global groups, keywords, cp, ex
    cp.set("monitor", "groups", ",".join(groups))
    cp.set("monitor", "keywords", ",".join(keywords))
    cp.write(open("./src/data/monitor/config.ini", "w"))
    ex.groups = groups
    ex.keywords = keywords

cp = configparser.ConfigParser()
groups = keywords = []
ex = export()

export = require("tools")
Translate = export.translate
DeltaStr = export.deltastr

scheduler = require('nonebot_plugin_apscheduler').scheduler

if not os.path.isdir("./src/data/monitor"):
    os.makedirs("./src/data/monitor")
if not os.path.isfile("./src/data/monitor/config.ini"):
    open("./src/data/monitor/config.ini", "w")
cp.read("./src/data/monitor/config.ini")
if not cp.has_section("monitor"):
    cp.add_section("monitor")
    cp.write(open("./src/data/monitor/config.ini", "w"))
if not cp.has_option("monitor", "groups"):
    cp.set("monitor", "groups", "")
    cp.write(open("./src/data/monitor/config.ini", "w"))
if not cp.has_option("monitor", "keywords"):
    cp.set("monitor", "keywords", "")
    cp.write(open("./src/data/monitor/config.ini", "w"))
if not cp.has_option("monitor", "id"):
    cp.set("monitor", "id", "")
    cp.write(open("./src/data/monitor/config.ini", "w"))


Load_Config()

enable_monitor = on_command("开启监控", permission=SUPERUSER)
disable_monitor = on_command("关闭监控", permission=SUPERUSER)
add_monitor = on_command("添加监控", permission=SUPERUSER)
del_monitor = on_command("删除监控", permission=SUPERUSER)

@enable_monitor.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group = event.group_id.__str__()
    global cp
    if group in groups:
        await enable_monitor.send("本群已在监控通知列表,请勿重复操作")
    else:
        groups.append(group)
        Save_Config()
        await enable_monitor.send("成功将本群添加到监控通知列表")

@disable_monitor.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group = event.group_id.__str__()
    global cp
    if group in groups:
        groups.remove(group)
        Save_Config()
        await disable_monitor.send("成功将本群移除监控通知列表")
    else:
        await disable_monitor.send("本群不在监控通知列表,无效操作")

@add_monitor.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    keyword = event.get_message().__str__().strip()
    print(keyword)
    global cp
    if keyword in keywords:
        await enable_monitor.send("关键词 [{0}] 已在监控列表, 请勿重复操作".format(keyword))
    else:
        keywords.append(keyword)
        Save_Config()
        await enable_monitor.send("成功将关键词 [{0}] 添加到监控列表".format(keyword))

@del_monitor.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    keyword = event.get_message().__str__().strip()
    global cp
    if keyword in keywords:
        keywords.remove(keyword)
        Save_Config()
        await disable_monitor.send("成功将关键词 [{0}] 移除监控列表".format(keyword))
    else:
        await disable_monitor.send("关键词 [{0}] 不在监控列表,无效操作".format(keyword))



alive = ilive = True

@scheduler.scheduled_job('cron', minute='*/1', id='alerts')
async def Alerts_Monitor():
    global alive
    try:
        response = requests.get(url="https://api.warframestat.us/pc/alerts")
        data = json.loads(response.text)
        if not len(data):
            alive = False
            print("[监控:警报]目前无警报")
            return
        flag = False
        for i in data:
            for j in keywords:
                if j.lower() in i["mission"]["reward"]["itemString"].lower() or j.lower() in Translate(i["mission"]["reward"]["itemString"], "dict").lower():
                    alive = True
                    if i["id"] not in cp.get("monitor", "id"):
                        flag = True

                        content = "监控到关键词 [{0}]".format(j)
                        content += "\n——————————"
                        #节点
                        content += "\n—节点: {0}".format(Translate(i["mission"]["node"], "dict"))

                        #模式
                        type = Translate(i["mission"]["type"], "dict")
                        content += "\n—模式: {0} ({1})".format(type, i["enemy"])

                        #奖励
                        reward = Translate(i["mission"]["reward"]["itemString"], "dict")
                        content += "\n—奖励: {0}".format(reward)

                        #剩余时间
                        utcTime = datetime.strptime(i["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
                        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
                        content += "\n—剩余时间: " + DeltaStr(timeLeft)

                        content += "\n——————————"

                        for k in groups:
                            await nonebot.get_bots().copy().popitem()[1].call_api("send_group_msg", **{
                                "message": content,
                                "group_id": k
                            })

                        print("[监控:警报]检测到监控关键词,已通知到群")
                        
                        cp.set("monitor", "id", cp.get("monitor", "id") + i["id"])
                        Save_Config()
        if not flag:
            print("[监控:警报]未检测到监控关键词")
            
            # 清除id数据待完善
            for i in data:
                if i["id"] in cp.get("monitor", "id"):
                    return
            alive = False
    except Exception as e:
        print("[监控:警报]获取失败 {0}".format(e))

@scheduler.scheduled_job('cron', minute='*/1', id='invasions')
async def Invasions_Monitor():
    global ilive
    try:
        response = requests.get(url="https://api.warframestat.us/pc/invasions")
        data = json.loads(response.text)
        flag = False
        for i in data:
            if i["completed"]:
                continue
            for j in keywords:
                if len(i["attackerReward"]["countedItems"]) and (j.lower() in i["attackerReward"]["countedItems"][0]["key"].lower() or j.lower() in Translate(i["attackerReward"]["countedItems"][0]["key"], "dict").lower()) or len(i["defenderReward"]["countedItems"]) and (j.lower() in i["defenderReward"]["countedItems"][0]["key"].lower() or j.lower() in Translate(i["defenderReward"]["countedItems"][0]["key"], "dict").lower()):
                    ilive = True
                    if i["id"] not in cp.get("monitor", "id"):
                        flag = True

                        content = "监控到关键词 [{0}]".format(j)
                        content += "\n——————————"

                        #节点、星球
                        content += "\n—节点: {0}".format(Translate(i["node"], "dict"))

                        #进攻方进度、派系、奖励
                        if len(i["attackerReward"]["countedItems"]):
                            i["attackerReward"]["countedItems"][0]["key"] = Translate(
                                i["attackerReward"]["countedItems"][0]["key"], "invasion")
                            content += "\n—进攻: {0}% {1}×{2}".format(
                                round(i["completion"], 1), i["attackerReward"]["countedItems"][0]["key"], i["attackerReward"]["countedItems"][0]["count"])
                        else:
                            content += "\n—进攻: {0}% 无".format(round(i["completion"], 1))

                        #防守方进度、派系、奖励
                        if len(i["defenderReward"]["countedItems"]):
                            i["defenderReward"]["countedItems"][0]["key"] = Translate(
                                i["defenderReward"]["countedItems"][0]["key"], "invasion")
                            content += "\n—防守: {0}% {1}×{2}".format(
                                round(100 - round(i["completion"], 1), 1), i["defenderReward"]["countedItems"][0]["key"], i["defenderReward"]["countedItems"][0]["count"])
                        else:
                            content += "\n—防守: {0}% 无".format(
                                round(100 - round(i["completion"], 1), 1))

                        content += "\n——————————"

                        for k in groups:
                            await nonebot.get_bots().copy().popitem()[1].call_api("send_group_msg", **{
                                "message": content,
                                "group_id": k
                            })

                        print("[监控:入侵]检测到监控关键词,已通知到群")

                        cp.set("monitor", "id", cp.get("monitor", "id") + i["id"])
                        Save_Config()
        if not flag:
            print("[监控:入侵]未检测到监控关键词")

            # 清除id数据待完善
            for i in data:
                if i["id"] in cp.get("monitor", "id"):
                    return
            ilive = False
    except Exception as e:
        print("[监控:入侵]获取失败 {0}".format(e))

@scheduler.scheduled_job('cron', second='*/10', id='dataClear')
async def Data_Clear():
    if not alive and not ilive and cp.get("monitor", "id") != "":
        cp.set("monitor", "id", "")
        Save_Config()
        print("[监控]监控数据已清理")

