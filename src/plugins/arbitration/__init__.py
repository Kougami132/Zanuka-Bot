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

arbitration = on_command("仲裁")

@arbitration.handle()
async def _(bot: Bot, event: Event):
    try:
        response = requests.get(url="https://api.warframestat.us/pc/arbitration")
        data = json.loads(response.text)

        result = "仲裁信息如下:"

        #节点、星球
        result += "\n节点: " + Translate(data["node"], "dict")
        
        #模式、派系
        data["type"] = Translate(data["type"], "dict")
        result += "\n任务: " + data["type"]
        result += "\n派系: " + data["enemy"]
        
        #剩余时间
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        result += "\n剩余时间: " + DeltaStr(timeLeft)
            
        await arbitration.send(result)
    except Exception as e:
        print(e)
        await arbitration.finish("获取失败,请重试!")
