from fuzzywuzzy import fuzz
from ..dict import get_dict
from ..warframemarket.match import is_all_eng


def matchRiven(riven: str):
    rivens = get_dict()["rivens"]
    similar = 32
    result = None
    node = "item_name" if is_all_eng(riven) else "zh_name"
    for i in rivens:
        if " " in riven:
            s = fuzz.ratio(riven.lower(), i[node].lower())
        else:
            s = fuzz.ratio(riven.lower(), i[node].lower().replace(" ", ""))
        if s > similar:
            similar = s
            result = i
    return result
