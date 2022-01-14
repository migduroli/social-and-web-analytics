import facebook
import requests
import json

with open("auth/facebook_credentials.json", "r") as file:
    credentials = json.load(file)


class FacebookAuth:
    BASE_URI = "https://www.facebook.com"
    GRAPH_URI = "https://graph.facebook.com"
    API_VERSION = "2.8"

    class App:
        CODE = None
        ACCESS_TOKEN = None

    @staticmethod
    def get_auth_url():
        url = (
            f"{FacebookAuth.BASE_URI}/v{FacebookAuth.API_VERSION}/dialog/oauth?"
            f"client_id={client_id}&"
            f"redirect_uri={url_redirect}&"
            f"state={state}"
        )
        return url

    @staticmethod
    def get_access_token(code: str) -> str:
        url = (
            f"{FacebookAuth.GRAPH_URI}/v{FacebookAuth.API_VERSION}/"
            f"oauth/access_token?"
            f"redirect_uri={url_redirect}"
            f"&client_id={client_id}"
            f"&client_secret={client_secret}"
            f"&code={code}"
        )
        return url


client_id = credentials["client_id"]
client_secret = credentials["client_secret"]
url_redirect_raw = credentials["url_redirect_raw"]
url_redirect = credentials["url_redirect"]
state = credentials["state"]

url_auth = FacebookAuth.get_auth_url()
print(f"Click here to get your App code:\n {url_auth}")
FacebookAuth.App.CODE = "YOUR_CODE"

url_access_token = FacebookAuth.get_access_token(FacebookAuth.App.CODE)

r = requests.get(url_access_token)

FacebookAuth.App.ACCESS_TOKEN = r.json()["access_token"]

graph = facebook.GraphAPI(
    access_token=FacebookAuth.App.ACCESS_TOKEN,
    version=FacebookAuth.API_VERSION
)

graph.get_object("me")

