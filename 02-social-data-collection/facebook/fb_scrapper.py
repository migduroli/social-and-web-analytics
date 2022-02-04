import facebook_scraper as fb

google_page = fb.get_page_info(account="Google")

# Try to get all:
for p in fb.get_posts("Google"):
    print(p)

fb.get_profile("JOEROGAN")