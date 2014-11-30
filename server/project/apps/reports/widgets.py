
def _safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0


def build_slider(expenditure, budget, color="#e5b744"):
    expenditure = _safe_float(expenditure)
    budget = _safe_float(budget)
    markers = []
    normalize = (expenditure+budget)/(2.0/1.1/2.0) or 1
    if budget and abs(expenditure-budget)/normalize < 0.1:
        text1 = " "
    elif budget == 0 and expenditure == 0:
        text1 = " "
    else:
        text1 = None
    if expenditure > budget:
        markers.append({ "bar-color": color, 
                         "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "value-text": text1 or 'R{:20,.0f}'.format(budget),
                         "position": budget/normalize })
        markers.append({ "bar-color": "#f04338", 
                         "marker-color": "#f04338", 
                         "marker-style": "long", 
                         "marker-text": "Actual", 
                         "value-text": 'R{:20,.0f}'.format(expenditure),
                         "position": expenditure/normalize })
    elif expenditure == budget:
        markers.append({ "bar-color": color, 
                         "marker-color": color, 
                         "marker-style": "long", 
                         "marker-text": "Actual",
                         "value-text": 'R{:20,.0f}'.format(expenditure),
                         "position": expenditure/normalize })
        markers.append({ "bar-color": "#e5b744", 
                         "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "value-text": text1 or 'R{:20,.0f}'.format(budget),
                         "position": budget/normalize })
    else:
        markers.append({ "bar-color": color, 
                         "marker-color": color, 
                         "marker-style": "long", 
                         "marker-text": "Actual", 
                         "value-text": 'R{:20,.0f}'.format(expenditure),
                         "position": expenditure/normalize })
        markers.append({ "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "value-text": text1 or 'R{:20,.0f}'.format(budget),
                         "position": budget/normalize })
    return markers

def build_slider_v2(expenditure, budget, color="#e5b744"):
    expenditure = _safe_float(expenditure / 1000000)
    budget = _safe_float(budget / 1000000)
    markers = []
    normalize = (expenditure+budget)/(2.0/1.1/2.0) or 1
    if budget and abs(expenditure-budget)/normalize < 0.1:
        text1 = " "
    elif budget == 0 and expenditure == 0:
        text1 = " "
    else:
        text1 = None
    format_str = 'R{:14,.0f}M'
    if expenditure > budget:
        markers.append({ "bar-color": color, 
                         "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "value-text": text1 or format_str.format(budget),
                         "position": budget/normalize })
        markers.append({ "bar-color": "#f04338", 
                         "marker-color": "#f04338", 
                         "marker-style": "long", 
                         "marker-text": "Actual", 
                         "value-text": format_str.format(expenditure),
                         "position": expenditure/normalize })
    elif expenditure == budget:
        markers.append({ "bar-color": color, 
                         "marker-color": color, 
                         "marker-style": "long", 
                         "marker-text": "Actual",
                         "value-text": format_str.format(expenditure),
                         "position": expenditure/normalize })
        markers.append({ "bar-color": "#e5b744", 
                         "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "value-text": text1 or format_str.format(budget),
                         "position": budget/normalize })
    else:
        markers.append({ "bar-color": color, 
                         "marker-color": color, 
                         "marker-style": "long", 
                         "marker-text": "Actual", 
                         "value-text": format_str.format(expenditure),
                         "position": expenditure/normalize })
        markers.append({ "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "value-text": text1 or format_str.format(budget),
                         "position": budget/normalize })
    return markers

def build_gauge(planned, actual, text1=None, text2=None):
    planned = _safe_float(planned)
    actual = _safe_float(actual)
    needles = []
    if abs(actual-planned) < 10:
        text1 = " "
    needles.append({ "needle-style": "dashed", 
                     "position": min(planned/100.0, 1), 
                     "text": text1 or "Planned" })
    needles.append({ "needle-color": [ "#86bf53", "#cce310" ], 
                     "needle-style": "plain", 
                     "position": min(actual/100.0, 1), 
                     "text": text2 or "Actual" })
    return needles

def build_donut(values, percentage=False):
    return {
        "as_percentage": percentage, 
        "values": [_safe_float(value) for value in values]
    }
