from datetime import timedelta
import re
from nonebot.plugin import export
import json

def Load_Dict():
    global WF_Dict, WF_Invasion, WF_Lib, WF_NightWave, WF_Sale, WF_Riven, WF_AllRiven, ex
    WF_Dict = json.loads(open("./src/data/wfa/WF_Dict.json", "rb").read())
    print("WF_Dict => " + len(WF_Dict).__str__())
    WF_Invasion = json.loads(open("./src/data/wfa/WF_Invasion.json", "rb").read())
    print("WF_Invasion => " + len(WF_Invasion).__str__())
    WF_Lib = json.loads(open("./src/data/wfa/WF_Lib.json", "rb").read())
    print("WF_Lib => " + len(WF_Lib).__str__())
    WF_NightWave = json.loads(open("./src/data/wfa/WF_NightWave.json", "rb").read())
    print("WF_NightWave => " + len(WF_NightWave).__str__())
    WF_Sale = json.loads(open("./src/data/wfa/WF_Sale.json", "rb").read())
    print("WF_Sale => " + len(WF_Sale).__str__())
    WF_Riven = json.loads(open("./src/data/wfa/WF_Riven.json", "rb").read())
    print("WF_Riven => " + len(WF_Riven).__str__())
    WF_AllRiven = json.loads(open("./src/data/wfa/WF_AllRiven.json", "rb").read())
    print("WF_AllRiven => " + len(WF_AllRiven).__str__())
    ex.dict, ex.invasion, ex.lib, ex.nightwave, ex.sale, ex.riven, ex.allriven = WF_Dict, WF_Invasion, WF_Lib, WF_NightWave, WF_Sale, WF_Riven, WF_AllRiven
def Translate(en, dictname):
    if dictname == "dict":
        dict = WF_Dict
    elif dictname == "invasion":
        dict = WF_Invasion
    elif dictname == "lib":
        dict = WF_Lib
    elif dictname == "nightwave":
        dict = WF_NightWave
    elif dictname == "sale":
        dict = WF_Sale
    elif dictname == "riven":
        dict = WF_Riven
    elif dictname == "allriven":
        dict = WF_AllRiven
    
    ptn1 = re.compile(r"[(](.+?)[)]")  # Stephano (Uranus)
    ptn2 = re.compile(r"^(.+?): (.+?)$")  # Enemy Physical Enhancement: Impact
    en1 = ptn1.findall(en)
    en2 = ptn2.findall(en)

    if len(en1):
        for i in dict:
            if en1[0] == i["en"]:
                return en.replace(en1[0], i["zh"])
    elif len(en2) and len(en2[0]) == 2:
        result = en
        flag = False
        for i in dict:
            if en2[0][0] == i["en"]:
                result = result.replace(en2[0][0], i["zh"])
                if flag:
                    break
                else:
                    flag = True
            if en2[0][1] == i["en"]:
                result = result.replace(en2[0][1], i["zh"])
                if flag:
                    break
                else:
                    flag = True
        return result
    else:
        for i in dict:
            if en == i["en"]:
                return i["zh"]
    return en
def DeltaStr(timeLeft: timedelta):
    days = timeLeft.days
    secondsLeft = timeLeft.seconds
    hours = secondsLeft // 3600
    secondsLeft = secondsLeft - 3600 * hours
    minutes = secondsLeft // 60
    seconds = secondsLeft - 60 * minutes
    return f"{days} 天 {hours} 时 {minutes} 分 {seconds} 秒" if days else f"{hours} 时 {minutes} 分 {seconds} 秒" if hours else f"{minutes} 分 {seconds} 秒" if minutes else f"{seconds} 秒"

WF_Dict = WF_Invasion = WF_Lib = WF_NightWave = WF_Sale = WF_Riven = WF_AllRiven = {}

ex = export()
ex.load_dict = Load_Dict
ex.translate = Translate
ex.deltastr = DeltaStr

Load_Dict()
