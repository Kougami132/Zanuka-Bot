from nonebot import on_command
from nonebot.plugin import require
from nonebot.adapters import Bot, Event, Message
from datetime import datetime, timedelta
import requests
import json
import re

export = require("tools")
Translate = export.translate
DeltaStr = export.deltastr

sortie = on_command("突击")

@sortie.handle()
async def _(bot: Bot, event: Event):
    try:
        response = requests.get(url="https://api.warframestat.us/pc/sortie")
        data = json.loads(response.text)
        result = "今日突击如下:"
        result += "\nBOSS: {0} ({1})".format(data["boss"], data["faction"])
        result += "\n——————————"
        for i in data["variants"]:

            #节点、星球
            result += "\n—节点: " + Translate(i["node"], "dict")

            #模式、环境
            type = Translate(i["missionType"], "dict")
            modifier = Translate(i["modifier"], "dict")
            result += "\n—任务: {0} ({1})".format(type, modifier)

            result += "\n——————————"
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n—剩余时间: " + DeltaStr(timeLeft)
        await sortie.send(result)
    except Exception as e:
        print(e)
        await sortie.finish("获取失败,请重试!")
