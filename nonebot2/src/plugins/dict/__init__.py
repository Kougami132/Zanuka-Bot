from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from aiocqhttp import ActionFailed
from ..util import get_data_path, writeJson
from .query import queryItem, queryRivenItem, queryDict
import json

path = get_data_path() + "config/"
items = rivens = userDict = []
extraDict = {
    "set": "一套"
}
update = on_regex(r"^update$")


def set_dict(itemsDict, rivensDict):
    global items, rivens
    items, rivens = itemsDict, rivensDict

def get_dict():
    global items, rivens
    return {
        "items": items,
        "rivens": rivens
    }

@update.handle()
async def _(bot: Bot, event: MessageEvent):
    global items, rivens
    try:
        old_item_num, old_riven_num = len(items), len(rivens)
        res = await queryItem()
        if not res[0]:
            await bot.send(event, MessageSegment.reply(event.message_id) + f"接口出错, 提示: {res[1]}")
            return
        items = res[1]["payload"]["items"]
        res = await queryRivenItem()
        if not res[0]:
            await bot.send(event, MessageSegment.reply(event.message_id) + f"接口出错, 提示: {res[1]}")
            return
        rivens = res[1]["payload"]["items"]
        res = await queryDict()
        if not res[0]:
            await bot.send(event, MessageSegment.reply(event.message_id) + f"接口出错, 提示: {res[1]}")
            return
        dictText = res[1]["query"]["pages"][0]["revisions"][0]["content"]
        userDict = json.loads(
                            dictText.replace(r"\n", "\n")
                                    .replace(r"\"", '"')
                                    .replace(r"\&", "&")
                                    .replace("-", " ")
                                    .replace("'", "")
                                    .lower()
                        )["text"]
        userDict.update(extraDict)
        new_item_num, new_riven_num = len(items), len(rivens)
        default_item_num = 0
        for i in range(len(items)):
            item_name = items[i]["url_name"].replace("_", " ")
            if item_name in userDict:
                items[i]["zh_name"] = userDict[item_name]
            else:
                before = item_name.split(' ')
                after = []
                for j in before:
                    if j in userDict:
                        after.append(userDict[j])
                    else:
                        after.append(j)
                items[i]["zh_name"] = " ".join(after).title()
                if after == before:
                    default_item_num += 1
        default_riven_num = 0
        for i in range(len(rivens)):
            riven_name = rivens[i]["url_name"].replace("_", " ").replace(" and ", " & ")
            if riven_name in userDict:
                rivens[i]["zh_name"] = userDict[riven_name]
            else:
                rivens[i]["zh_name"] = riven_name.title()
                default_riven_num += 1
        await writeJson(items, path + "WF_Items.ini")
        await writeJson(rivens, path + "WF_Rivens.ini")
        await bot.send(event, f"Done!\nWF_Items: {old_item_num} => {new_item_num} ({default_item_num} untranslated)\nWF_Rivens: {old_riven_num} => {new_riven_num} ({default_riven_num} 条未翻译)")
    except ActionFailed:
        await bot.send(event, MessageSegment.reply(event.message_id) + '账号可能被风控, 请重试!')
    except Exception as e:
        await bot.send(event, MessageSegment.reply(event.message_id) + f'程序出错：{e}')


