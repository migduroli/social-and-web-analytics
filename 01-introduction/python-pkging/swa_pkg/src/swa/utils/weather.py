import requests

# To know more about the weather URL: "https://wttr.in/:help
WEATHER_URL = "https://wttr.in/"
DEFAULT_CITY = "madrid"


def get_weather_conditions(city_name: str) -> dict:
    """Gets the weather conditions via https://wttr.in

    :param city_name: Name of the city

    :return: dict {city_name: response.text}
    """
    url = WEATHER_URL if not city_name else f"{WEATHER_URL}/{city_name}"
    response = requests.get(url)
    data = {}

    if response.status_code == requests.status_codes.codes.ALL_GOOD:
        # Cambiamos la firma de @igor_chibi:
        signature = "Follow \x1b[46m\x1b[30m@igor_chubin\x1b[0m for wttr.in updates"
        color_open = "\x1b[46m\x1b[30m"
        color_close = "\x1b[0m"
        text = response.text.replace(
            signature,
            f"This is {color_open}Social and Web Analytics{color_close} in live!"
        )
        data[city_name] = text
    else:
        print(f"Error colectando datos, status_code = {response.status_code}")
        data[city_name] = None
    return data
