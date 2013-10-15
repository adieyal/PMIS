import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# TODO - need to write a test for this
def format_number(value):
    try:
        if value == int(value):
            return locale.format("%d", value, grouping=True)
        else:
            return locale.format("%.2f", value, grouping=True)
    except ValueError:
        return "-"

def format_currency(value):
    try:
        if int(value) == 0:
            return "R0.00"
        else:
            return "R" + format_number(value)
    except ValueError:
        return "-"

def format_percentage(value):
    try:
        if int(value) == value:
            return "%d%%" % value
        else:
            return "%.1f%%" % value
    except ValueError:
        return "-"

