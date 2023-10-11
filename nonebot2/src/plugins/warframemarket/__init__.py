from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from aiocqhttp import ActionFailed
from datetime import datetime, timedelta
from .match import matchItem
from .query import queryWarframeMarket
from .sort import sortWarframeMarket
from ..util import forward_msg


wm = on_command("wm")


@wm.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    async def send_error(msg: str):
        await bot.send(event, MessageSegment.reply(event.message_id) + msg)
    try:
        item = arg.extract_plain_text().strip()
        if item == "":
            await send_error("参数不能为空")
            return
        # 参数分离
        item = item.replace("，", ",")
        mod_rank = 0
        if "," in item:
            mod_rank = item.split(",")[1]
            if not mod_rank.isdigit():
                await send_error("参数错误")
                return
            mod_rank = int(mod_rank)
            item = item.split(",")[0]
        # 模糊匹配
        item = matchItem(item)
        if item == None:
            await send_error("未找到该物品, 请缩小范围")
            return
        # 请求数据
        if mod_rank:
            await bot.send(event, f"正在查询 [{item['zh_name']} ({mod_rank} 级)] 价格, 请稍等")
        else:
            await bot.send(event, f"正在查询 [{item['zh_name']}] 价格, 请稍等")
        res = await queryWarframeMarket(item["url_name"])
        data = res["payload"]["orders"]
        # 筛选
        data = [i for i in data if 
                i["visible"] and 
                i["user"]["status"] == "ingame" and 
                i["order_type"] == "sell" and 
                ("mod_rank" not in i or i["mod_rank"] >= mod_rank)]
        # 排序
        data = sortWarframeMarket(data)
        # 处理消息
        nodes = [f"查价物品: {item['zh_name']} ({item['item_name']})\n数据来源: https://warframe.market/items/{item['url_name']}"]
        content = "".center(30, "—")
        for i in data:
            is_mod = "mod_rank" in i
            if is_mod:
                content += "\n—单价: {0} —数量: {1} —等级: {2} —卖家: {3} —声誉: {4}".format(
                    int(i["platinum"]), i["quantity"], i["mod_rank"], i["user"]["ingame_name"], i["user"]["reputation"])
            else:
                content += "\n—单价: {0} —数量: {1} —卖家: {2} —声誉: {3}".format(
                    int(i["platinum"]), i["quantity"], i["user"]["ingame_name"], i["user"]["reputation"])
        content += "\n" + "".center(30, "—")
        nodes.append(content)
        for i in data:
            content = "".center(30, "—")
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
            content += "\n" + "".center(30, "—")
            if is_mod:
                content += "\n/w {0} Hi! I want to buy: {1} (rank {2}) for {3} platinum. (warframe.market)".format(
                    i["user"]["ingame_name"], item["item_name"], i["mod_rank"], i["platinum"])
            else:
                content += "\n/w {0} Hi! I want to buy: {1} for {2} platinum. (warframe.market)".format(
                    i["user"]["ingame_name"], item["item_name"], i["platinum"])
            nodes.append(content)
        messages = forward_msg(nodes, bot.self_id, "ZANUKA")
        await bot.send_group_forward_msg(group_id=event.group_id, messages=messages)
    except ActionFailed as e:
        await send_error("账号可能被风控, 请重试!")
    except FileNotFoundError as e:
        await send_error(f"素材丢失: {e}")
    except Exception as e:
        await send_error(f"程序出错：{type(e)}, {e}")
