from fuzzywuzzy import fuzz
from ..dict import get_dict


def is_all_eng(text: str):
    import string
    for i in text:
        if i not in string.ascii_lowercase + string.ascii_uppercase:
            return False
    return True

def matchItem(item: str):
    items = get_dict()["items"]
    similar = 32
    result = None
    node = "item_name" if is_all_eng(item) else "zh_name"
    for i in items:
        if " " in item:
            s = fuzz.ratio(item.lower(), i[node].lower())
        else:
            s = fuzz.ratio(item.lower(), i[node].lower().replace(" ", ""))
        if s > similar:
            similar = s
            result = i
    return result
