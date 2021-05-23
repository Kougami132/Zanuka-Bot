from nonebot import on_command
from nonebot.plugin import require
from nonebot.adapters.cqhttp import Bot, Event
from datetime import datetime, timedelta
import requests
import json
import re
import copy

export = require("tools")
Translate = export.translate
DeltaStr = export.deltastr

nightwave = on_command("电波")

@nightwave.handle()
async def _(bot: Bot, event: Event):
    try:
        response = requests.get(url="https://api.warframestat.us/pc/nightwave")
        data = json.loads(response.text)
        nodes = []
        node = {
            "type": "node",
            "data": {
                "uin": f"{bot.self_id}",
                "name": "ZANUKA"
            }
        }
        for i in data["activeChallenges"]:
            content = "——————————"

            #任务标题与描述
            i["title"] = Translate(i["title"], "nightwave")
            content += "\n—[{0}] {1}".format(i["reputation"], i["title"])
            i["desc"] = Translate(i["desc"], "nightwave")
            content += "\n—任务: {0}".format(i["desc"])
            
            #剩余时间
            utcTime = datetime.strptime(i["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
            timeLeft = utcTime + timedelta(hours=8) - datetime.now()
            content += "\n—剩余时间: " + DeltaStr(timeLeft)
                
            content += "\n——————————"
            node["data"]["content"] = content
            nodes.append(copy.deepcopy(node))
        
        #本季剩余时间
        utcTime = datetime.strptime(data["expiry"], "%Y-%m-%dT%H:%M:%S.%fZ")
        timeLeft = utcTime + timedelta(hours=8) - datetime.now()
        node["data"]["content"] = f"本季电波剩余时间: " + DeltaStr(timeLeft)
        nodes.append(copy.deepcopy(node))
        await bot.send_group_forward_msg(group_id=event.group_id, messages=nodes)
    except Exception as e:
        print(e)
        await nightwave.finish("获取失败,请重试!")
