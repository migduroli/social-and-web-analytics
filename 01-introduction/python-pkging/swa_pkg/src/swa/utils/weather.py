import requests

WHEATHER_URL = "https://wttr.in/"

def get_wheather_conditions(citi_name: str = None) -> str:
    """Gets the wheather conditions vias wttr.in
    :return: Json
    """
    url = WHEATHER_URL \
        if not citi_name \
        else f"{WHEATHER_URL}/{citi_name}"
    response = requests.get(url)
    signature = "Follow \x1b[46m\x1b[30m@igor_chubin\x1b[0m for wttr.in updates"
    color_open = "\x1b[46m\x1b[30m"
    color_close = "\x1b[0m"
    return response.text.replace(
        signature,
        f"This is {color_open}Social and Web Analytics{color_close} in live!"
    )
