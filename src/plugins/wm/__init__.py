import copy
from os import truncate
from nonebot import on_command
from nonebot.plugin import require
from nonebot.adapters import Bot, Event, Message
from datetime import datetime, timedelta
import requests
import json
from fuzzywuzzy import fuzz

export = require("tools")
WF_Sale = export.sale

wm = on_command("wm", aliases={"WM"})

@wm.handle()
async def _(bot: Bot, event: Event):
    try:
        item = event.get_message().__str__().strip()
        if item == "":
            await wm.send("参数不能为空!")
            return
        
        #物品等级分离
        item = item.replace("，", ",")
        mod_rank = 0
        if "," in item:
            mod_rank = item.split(",")[1]
            if not mod_rank.isdigit():
                await wm.send("参数错误")
            mod_rank = int(mod_rank)
            item = item.split(",")[0]

        #相似度匹配
        index = 0
        similar = 0
        for i in range(len(WF_Sale)):
            if " " in item:
                s = fuzz.ratio(item,WF_Sale[i]["zh"])
            else:
                s = fuzz.ratio(item,WF_Sale[i]["zh"].replace(" ", ""))
            if s > similar:
                similar = s
                index = i
        if similar < 50:
            await wm.send("未找到该物品,请缩小范围!")
            return
        
        await wm.send("正在查询 [{0}] 价格,请稍等".format(WF_Sale[index]["zh"]))
        response = requests.get(url="https://api.warframe.market/v1/items/{0}/orders".format(WF_Sale[index]["code"]))
        data = json.loads(response.text)

        #筛选并排序
        rank = []
        for i in data["payload"]["orders"]:
            if not i["visible"] or i["user"]["status"] != "ingame" or i["order_type"] != "sell" or "mod_rank" in i.keys() and i["mod_rank"] < mod_rank:
                continue
            if not len(rank):
                rank.append(i)
                continue
            for j in range(len(rank)):
                if i["platinum"] <= rank[len(rank) - 1 - j]["platinum"]:
                    if (len(rank) - 1 - j) == 0:
                        rank.insert(len(rank) - 1 - j, i) 
                        break
                    else:
                        continue
                else:
                    rank.insert(len(rank) - j, i)
                    break
            if len(rank) > 10:
                del rank[len(rank) - 1]

        nodes = []
        node = {
            "type": "node",
            "data": {
                "uin": f"{bot.self_id}",
                "name": "ZANUKA"
            }
        }
        node["data"]["content"] = "查价物品: {0} ({1})\n数据来源: https://warframe.market/items/{2}".format(
            WF_Sale[index]["zh"], WF_Sale[index]["en"], WF_Sale[index]["code"])
        nodes.append(copy.deepcopy(node))

        #简略
        is_mod = False
        content = "——————————————————————————————"
        for i in rank:
            if "mod_rank" in i.keys():
                is_mod = True
            if is_mod:
                content += "\n—单价: {0} —数量: {1} —等级: {2} —卖家: {3} —声誉: {4}".format(
                    int(i["platinum"]), i["quantity"], i["mod_rank"], i["user"]["ingame_name"], i["user"]["reputation"])
            else:
                content += "\n—单价: {0} —数量: {1} —卖家: {2} —声誉: {3}".format(
                    int(i["platinum"]), i["quantity"], i["user"]["ingame_name"], i["user"]["reputation"])
        content += "\n——————————————————————————————"
        node["data"]["content"] = content
        nodes.append(copy.deepcopy(node))

        #详细
        for i in rank:
            content = "——————————————————————————————"
            if is_mod:
                content += "\n—单价: {0} —数量: {1} —等级: {2}".format(
                    int(i["platinum"]), i["quantity"], i["mod_rank"])
            else:
                content += "\n—单价: {0} —数量: {1}".format(
                    int(i["platinum"]), i["quantity"])
            content += "\n—卖家: {0} —声誉: {1} —地区: {2}".format(
                i["user"]["ingame_name"], i["user"]["reputation"], i["user"]["region"])
            utcTime = datetime.strptime(i["creation_date"], "%Y-%m-%dT%H:%M:%S.%f+00:00")
            localTime = (utcTime + timedelta(hours=8)).strftime("%Y 年 %m 月 %d 日 %H:%M:%S")
            content += "\n—创建时间: " + localTime
            utcTime = datetime.strptime(i["last_update"], "%Y-%m-%dT%H:%M:%S.%f+00:00")
            localTime = (utcTime + timedelta(hours=8)).strftime("%Y 年 %m 月 %d 日 %H:%M:%S")
            content += "\n—上次更新: " + localTime
            utcTime = datetime.strptime(i["user"]["last_seen"], "%Y-%m-%dT%H:%M:%S.%f+00:00")
            localTime = (utcTime + timedelta(hours=8)).strftime("%Y 年 %m 月 %d 日 %H:%M:%S")
            content += "\n—上次来看: " + localTime
            content += "\n——————————————————————————————"
            if is_mod:
                content += "\n/w {0} Hi! I want to buy: {1} (rank {2}) for {3} platinum. (warframe.market)".format(
                    i["user"]["ingame_name"], WF_Sale[index]["en"], i["mod_rank"], i["platinum"])
            else:
                content += "\n/w {0} Hi! I want to buy: {1} for {2} platinum. (warframe.market)".format(
                    i["user"]["ingame_name"], WF_Sale[index]["en"], i["platinum"])
            node["data"]["content"] = content
            nodes.append(copy.deepcopy(node))
        
        await bot.send_group_forward_msg(group_id=event.group_id, messages=nodes)
    except Exception as e:
        print(e)
        await wm.finish("获取失败,请重试!")
