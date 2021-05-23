from nonebot import on_command
from nonebot.adapters import Bot, Event
import requests
import json
from datetime import datetime, timedelta
from nonebot.plugin import require

export = require("tools")
DeltaStr = export.deltastr

earth = on_command("地球时间")
cetus = on_command("平原时间")
vallis = on_command("山谷时间")
cambion = on_command("幽都时间")

@earth.handle()
async def _(bot: Bot, event: Event):
    try:
        response = requests.get(url="https://api.warframestat.us/pc/earthCycle")
        data = json.loads(response.text)
        result = "Zanuka为恁报时:"
        result += "\n地球状态: 白天" if data["isDay"] else "\n地球状态: 夜晚"
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n剩余时间: " + DeltaStr(timeLeft)
        await earth.send(result)
    except Exception as e:
        print(e)
        await earth.finish("获取失败,请重试!")

@cetus.handle()
async def _(bot: Bot, event: Event):
    try:
        response = requests.get(url="https://api.warframestat.us/pc/cetusCycle")
        data = json.loads(response.text)
        result = "Zanuka为恁报时:"
        result += "\n平原状态: 白天" if data["isDay"] else "\n平原状态: 夜晚"
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n剩余时间: " + DeltaStr(timeLeft)
        await cetus.send(result)
    except Exception as e:
        print(e)
        await cetus.finish("获取失败,请重试!")

@vallis.handle()
async def _(bot: Bot, event: Event):
    try:
        response = requests.get(url="https://api.warframestat.us/pc/vallisCycle")
        data = json.loads(response.text)
        result = "Zanuka为恁报时:"
        result += "\n山谷状态: 温暖" if data["isWarm"] else "\n山谷状态: 寒冷"
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n剩余时间: " + DeltaStr(timeLeft)
        await vallis.send(result)
    except Exception as e:
        print(e)
        await vallis.finish("获取失败,请重试!")

@cambion.handle()
async def _(bot: Bot, event: Event):
    try:
        response = requests.get(url="https://api.warframestat.us/pc/cambionCycle")
        data = json.loads(response.text)
        result = "Zanuka为恁报时:"
        result += f"\n幽都状态: {str(data['active']).upper()}"
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n剩余时间: " + DeltaStr(timeLeft)
        await cambion.send(result)
    except Exception as e:
        print(e)
        await cambion.finish("获取失败,请重试!")
