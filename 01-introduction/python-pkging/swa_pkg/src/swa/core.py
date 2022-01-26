"""This is a simple wrapper of https://wttr.in to access the weather with Python.
"""
from swa.utils.weather import get_weather_conditions, DEFAULT_CITY


def salute(name: str = None) -> str:
    """Returns a salute message
    :return:
    """
    person = "world" if not name else name
    message = f"hello {person}!"
    return message


def the_weather(cities: list) -> dict:
    """Gets the weather conditions of a list of cities

    :return: Dictionary with the weather conditions
    """
    data = {}
    for city in cities:
        city_data = get_weather_conditions(
            city_name=city
        )
        data = {**data, **city_data}
    return data


def my_weather() -> str:
    """Gets the weather conditions of my region (via IP location)
    :return: string to be printed in console
    """
    data = get_weather_conditions(city_name=DEFAULT_CITY)
    return data[DEFAULT_CITY]
