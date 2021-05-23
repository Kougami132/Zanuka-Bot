from nonebot import on_command
from nonebot.plugin import require
from nonebot.adapters import Bot, Event, Message
from datetime import datetime, timedelta
import requests
import json

export = require("tools")
Translate = export.translate
DeltaStr = export.deltastr

dailydeals = on_command("特价")

@dailydeals.handle()
async def _(bot: Bot, event: Event):
    try:
        response = requests.get(url="https://api.warframestat.us/pc/dailyDeals")
        data = json.loads(response.text)
        result = "今日特价商品如下:\n——————————"
        for i in data:

            #商品、价格、数量
            i["item"] = Translate(i["item"], "dict")
            result += "\n—商品: " + i["item"]
            result += "\n—价格: {0} ({1})".format(i["salePrice"], i["originalPrice"])
            result += "\n—数量: {0}/{1}".format(i["total"] - i["sold"], i["total"])

            #剩余时间
            utcTime = datetime.strptime(
            i["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
            timeLeft = utcTime + timedelta(hours=8) - datetime.now()
            result += "\n—剩余时间: " + DeltaStr(timeLeft)
                
            result += "\n——————————"
        await dailydeals.send(result)
    except Exception as e:
        print(e)
        await dailydeals.finish("获取失败,请重试!")
