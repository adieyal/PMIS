clientcolors = {
    "DoE" :"#9792b3",
    "DCSR" :"#e7bb5e",
    "DEDET" :"#e4cfbf",
    "DoH" :"#8cc6ec",
    "DSD" :"#b9b387",
    "DSSL" :"#bd7794"
}

red = "#f04338"
grey = "#656263"

def dashboard_gauge(val1, val2, text1=None, text2=None):
    position1 = {
        "text" : text1 or "Planned",
        "needle-style" : "dashed",
        "position" : val1
    }

    position2 = {
        "text" : text2 or "Actual",
        "needle-style" : "plain",
        "needle-color": ["#86bf53", "#cce310"],
        "position" : val2
    }

    return [
        position1,
        position2,
    ]

def dashboard_slider(val1, val2, client, threshold=0.1, text1=None, text2=None, min_val=0.1, max_val=0.9):
    if (val1 < min_val): val1 = min_val
    if (val2 < min_val): val2 = min_val
    if (val1 > max_val): val1 = max_val
    if (val2 > max_val): val2 = max_val

    barcolor2 = clientcolors.get(client, "")
    if (val2 - val1 > threshold):
        barcolor2 = red

    barcolor1 = clientcolors.get(client, "")
    if (val1 - val2 > threshold): 
        barcolor1 = red

    text1 = text1 or "Planned"
    text2 = text2 or "Actual"
    if abs(val1 - val2) < 0.1:
        text1 = ""

    el1 = {
        "position": val1,
        "bar-color": barcolor1,
        "marker-color": grey,
        "marker-style": "short",
        "marker-text": text1,
    } 

    el2 = {
        "position": val2,
        "bar-color": barcolor2,
        "marker-color": red,
        "marker-style": "long",
        "marker-text": text2,
    } 

    if val1 > val2:
        return [el2, el1]
    else:
        return [el1, el2]
