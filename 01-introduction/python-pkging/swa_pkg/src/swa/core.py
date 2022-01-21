"""Some doc string
"""
from swa.utils.weather import get_wheather_conditions

def salute(name: str = None) -> str:
    """Returns a salute message
    :return:
    """
    person = "world" if not name else name
    message = f"hello {person}!"
    return message


def my_weather() -> str:
    """Gets the weather conditions of my region (via IP location)
    :return: Json with the weather conditions
    """
    conditions = get_wheather_conditions()
    return conditions