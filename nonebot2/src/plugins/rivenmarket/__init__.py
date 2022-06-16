from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from aiocqhttp import ActionFailed
from .match import matchRiven
from .query import queryRivenMarket
from ..util import forward_msg


rm = on_command("rm")


@rm.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    async def send_error(msg: str):
        await bot.send(event, MessageSegment.reply(event.message_id) + msg)
    try:
        riven = arg.extract_plain_text().strip()
        if riven == "":
            await send_error("参数不能为空")
            return
        # 模糊匹配
        riven = matchRiven(riven)
        if riven == None:
            await send_error("未找到该物品, 请缩小范围")
            return
        # 请求数据
        await bot.send(event, f"正在查询 [{riven['zh_name']}] 紫卡价格,请稍等")
        try:
            res = await queryRivenMarket(riven["url_name"])
        except Exception as e:
            await send_error(f"接口出错, 提示: {type(e)}")
            return
        data = res
        # 处理消息
        nodes = [f"查价武器: {riven['zh_name']} ({riven['item_name']})\n数据来源: https://riven.market/list/PC/{riven['url_name']}"]
        content = "".center(30, "—")
        for i in data:
            content += f"\n—单价: {i['price']} —次数: {i['rerolls']} —段位: {i['mr']} —等级: {i['rank']} —卖家: {i['seller']}"
        content += "\n" + "".center(30, "—")
        nodes.append(content)
        for i in data:
            content = "".center(30, "—")
            content += f"\n—单价: {i['price']} —次数: {i['rerolls']} —段位: {i['mr']} —等级: {i['rank']} —极性: {i['polarity']}"
            content += f"\n—卖家: {i['seller']} —卡名: {i['weapon']} {i['name']}"
            content += f"\n—词条: {i['stat1']} + {i['stat1val']} | {i['stat2']} + {i['stat2val']}"
            content += f" | {i['stat3']} + {i['stat3val']}" if i['stat3'] != "" else ""
            content += f" | {i['stat4']} - {i['stat4val']}" if i['stat4'] != "" else ""
            content += "\n" + "".center(30, "—")
            content += f"\n/w {i['seller']} Hey! I'd like to buy the {i['weapon']} {i['name']} Riven that you sell on Riven.market for {i['price']} Platinum!"
            nodes.append(content)
        messages = forward_msg(nodes, bot.self_id, "ZANUKA")
        await bot.send_group_forward_msg(group_id=event.group_id, messages=messages)


        
    except ActionFailed as e:
        await send_error("账号可能被风控, 请重试!")
    except FileNotFoundError as e:
        await send_error(f"素材丢失: {e}")
    except Exception as e:
        await send_error(f"程序出错：{e}")