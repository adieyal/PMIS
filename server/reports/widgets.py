
def _safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0

def build_slider_v3(planned, actual, budget):
    adjustment = 0.8

    planned = _safe_float(planned)
    actual = _safe_float(actual)
    budget = _safe_float(budget)

    if actual < planned:
        ouDirection = 'under'
    else:
        ouDirection = 'over'

    ouPercentage = (planned - actual) / planned * 100;

    default_color = '#e5b744'

    planned_colors = {
        'bar': default_color,
        'marker': '#656263',
    }

    if actual > planned:
        actual_colors = {
            'bar': '#f04338',
            'marker': '#f04338',
        }
    else:
        actual_colors = {
            'bar': default_color,
            'marker': default_color,
        }

    format_str = 'R{:14,.1f}M'

    payload = {
        'budget': {
            'title': 'Total Budget',
            'position': adjustment,

        },
        'planned': {
            'title': 'Planned',
            'percentage': planned / budget * 100,
            'text': format_str.format(planned),
            'position': planned / budget * adjustment,
            'bar': planned_colors['bar'],
            'marker': planned_colors['marker'],
        },
        'actual': {
            'title': 'Actual',
            'percentage': actual / budget * 100,
            'text': format_str.format(actual),
            'position': actual / budget * adjustment,
            'bar': actual_colors['bar'],
            'marker': actual_colors['marker'],
        },
        'over-under': {
            'direction': ouDirection,
            'percentage': ouPercentage,
        }
    }

    return payload

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
        markers.append({ "bar-color": color,
                         "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "value-text": text1 or 'R{:20,.0f}'.format(budget),
                         "position": budget/normalize })
    return markers

def build_slider_v2(expenditure, budget, color="#e5b744"):
    if budget == 0:
        expenditurePercentage = 'Undefined'
    else:
        expenditurePercentage = '%s%%' % int(expenditure / budget * 100)

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

    format_str = 'R{:14,.1f}M'
    if expenditure > budget:
        markers.append({ "bar-color": color, 
                         "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "value-text": text1 or format_str.format(budget),
                         "value": budget,
                         "percentage-text": '100%',
                         "position": budget/normalize })
        markers.append({ "bar-color": "#f04338", 
                         "marker-color": "#f04338", 
                         "marker-style": "long", 
                         "marker-text": "Actual", 
                         "value-text": format_str.format(expenditure),
                         "value": expenditure,
                         "percentage-text": expenditurePercentage,
                         "position": expenditure/normalize })
    elif expenditure == budget:
        markers.append({ "bar-color": color, 
                         "marker-color": color, 
                         "marker-style": "long", 
                         "marker-text": "Actual",
                         "value-text": format_str.format(expenditure),
                         "percentage-text": expenditurePercentage,
                         "value": expenditure,
                         "position": expenditure/normalize })
        markers.append({ "bar-color": "#e5b744", 
                         "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "value-text": text1 or format_str.format(budget),
                         "value": budget,
                         "percentage-text": '100%',
                         "position": budget/normalize })
    else:
        markers.append({ "bar-color": color, 
                         "marker-color": color, 
                         "marker-style": "long", 
                         "marker-text": "Actual", 
                         "value-text": format_str.format(expenditure),
                         "value": expenditure,
                         "percentage-text": expenditurePercentage,
                         "position": expenditure/normalize })
        markers.append({ "bar-color": color,
                         "marker-color": "#656263", 
                         "marker-style": "short", 
                         "marker-text": text1 or "Budget", 
                         "value-text": text1 or format_str.format(budget),
                         "value": budget,
                         "percentage-text": '100%',
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
