import json
import facebook_scraper as fb

google_page = fb.get_page_info(account="Google")

with open("auth/fb_cookies.json") as f:
    cookies = json.load(f)

fb.set_cookies(cookies)

# Try to get all:
for p in fb.get_posts("Google"):
    print(p)

fb.get_profile("JOEROGAN", friends=True)