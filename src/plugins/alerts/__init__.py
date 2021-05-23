from nonebot.plugin import on_command, require
from nonebot.adapters.cqhttp import Bot, Event
from datetime import datetime, timedelta
import requests
import json
import re
import copy

export = require("tools")
Translate = export.translate
DeltaStr = export.deltastr

alerts = on_command("警报")

@alerts.handle()
async def _(bot: Bot, event: Event):
    try:
        response = requests.get(url="https://api.warframestat.us/pc/alerts")
        data = json.loads(response.text)
        if not len(data):
            await alerts.send("目前无警报")
            return
        nodes = []
        node = {
            "type": "node",
            "data": {
                "uin": f"{bot.self_id}",
                "name": "ZANUKA"
            }
        }
        for i in data:
            content = "——————————"

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
            node["data"]["content"] = content
            nodes.append(copy.deepcopy(node))
            print(content)
        await bot.send_group_forward_msg(group_id=event.group_id, messages=nodes)
    except Exception as e:
        print(e)
        await alerts.finish("获取失败,请重试!")
