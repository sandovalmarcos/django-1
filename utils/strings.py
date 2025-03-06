
def is_positive_number(value):
    try:
        float_value = float(value)
    except ValueError:
        return False
    return float_value > 0
