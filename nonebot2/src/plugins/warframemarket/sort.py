

def sortWarframeMarket(data, num=10):
    rank = []
    for i in data:
        if not len(rank):
            rank.append(i)
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
        if len(rank) > num:
            del rank[len(rank) - 1]
    return rank