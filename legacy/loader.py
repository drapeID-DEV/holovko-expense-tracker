import json

def process(f):
    file = open(f)
    d = json.loads(file.read())
    res = []
    i = 0

    while i < len(d):
        item = d[i]

        if item["title"] != None and item["title"] != "":
            t = item["title"]
            t2 = ""

            for c in range(len(t)):
                t2 = t2 + t[c].lower()

            t2 = " ".join(t2.split())
            amount = 0

            try:
                amount = int(item["amount"])
            except:
                amount = 0

            res.append([t2, item["category"], amount, item["city"]])

        i = i + 1

    res2 = []
    for x in range(len(res)):
        found = False

        for y in range(len(res2)):
            if res2[y][0] == res[x][0] and res2[y][1] == res[x][1]:
                found = True

        if found == False:
            res2.append(res[x])

    st = {}

    for x in range(len(res2)):
        c = res2[x][3]

        if c in st.keys():
            st[c] = st[c] + 1
        else:
            st[c] = 1

    print(st)
    return res2