from constants import COUNT_ROOMS


def rn(x):
    """
    Checks if there is a number between the minimum
    and maximum values of rooms in the hotel
    """
    try:
        return 0 < int(x) <= COUNT_ROOMS
    except (TypeError, ValueError):
        return False
