from nonebot import get_driver
from .dict import path, set_dict
from .util import readJson


driver = get_driver()


@driver.on_startup
async def _():
    items = await readJson(path + "WF_Items.ini")
    rivens = await readJson(path + "WF_Rivens.ini")
    set_dict(items, rivens)