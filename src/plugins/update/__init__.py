import os
from nonebot.adapters import Bot, Event, Message
from nonebot.permission import SUPERUSER
from nonebot.plugin import export, on_command, require
import requests

export = require("tools")
WF_Dict, WF_Invasion, WF_Lib, WF_NightWave, WF_Sale, WF_Riven, WF_AllRiven = export.dict, export.invasion, export.lib, export.nightwave, export.sale, export.riven, export.allriven
Load_Dict = export.load_dict

update = on_command("update", permission=SUPERUSER)
reload = on_command("reload", permission=SUPERUSER)

@update.handle()
async def _(bot: Bot, event: Event):
    try:
        if not os.path.exists("./src/data/wfa/"):
            os.makedirs("./src/data/wfa/")

        dict = requests.get(
            url="https://raw.githubusercontent.com/Richasy/WFA_Lexicon/WFA5/WF_Dict.json", verify=False)
        open("./src/data/wfa/WF_Dict.json", "wb").write(dict.content)

        invasion = requests.get(
            url="https://raw.githubusercontent.com/Richasy/WFA_Lexicon/WFA5/WF_Invasion.json", verify=False)
        open("./src/data/wfa/WF_Invasion.json", "wb").write(invasion.content)

        lib = requests.get(
            url="https://raw.githubusercontent.com/Richasy/WFA_Lexicon/WFA5/WF_Lib.json", verify=False)
        open("./src/data/wfa/WF_Lib.json", "wb").write(lib.content)

        nightWave = requests.get(
            url="https://raw.githubusercontent.com/Richasy/WFA_Lexicon/WFA5/WF_NightWave.json", verify=False)
        open("./src/data/wfa/WF_NightWave.json", "wb").write(nightWave.content)

        sale = requests.get(
            url="https://raw.githubusercontent.com/Richasy/WFA_Lexicon/WFA5/WF_Sale.json", verify=False)
        open("./src/data/wfa/WF_Sale.json", "wb").write(sale.content)

        riven = requests.get(
            url="https://raw.githubusercontent.com/Richasy/WFA_Lexicon/WFA5/WF_Riven.json", verify=False)
        open("./src/data/wfa/WF_Riven.json", "wb").write(riven.content)

        allRiven = requests.get(
            url="https://raw.githubusercontent.com/Richasy/WFA_Lexicon/WFA5/WF_AllRiven.json", verify=False)
        open("./src/data/wfa/WF_AllRiven.json", "wb").write(allRiven.content)

        Load_Dict()
        await update.send(
            "Done!\nWF_Dict => {0}\nWF_Invasion => {1}\nWF_Lib => {2}\nWF_NightWave => {3}\nWF_Sale => {4}\nWF_Riven => {5}\nWF_AllRiven => {6}"
            .format(len(WF_Dict), len(WF_Invasion), len(WF_Lib), len(WF_NightWave), len(WF_Sale), len(WF_Riven), len(WF_AllRiven)))
    except Exception as e:
        print(e)
        await update.finish("Error!" + e.__str__())
