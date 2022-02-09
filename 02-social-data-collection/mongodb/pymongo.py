import facebook_scraper as fb
from pymongo import MongoClient, errors

client = MongoClient("localhost:27017")

db = client["scraping"]
db_fb = db["facebook"]

# Insert:
for post in fb.get_posts("google", pages=1):
    post_id = post.pop("post_id")
    record = {**post, "_id": post_id}
    try:
        db_fb.insert_one(record)
        print(f"Post inserted: {post_id}")
    except errors.DuplicateKeyError:
        db_fb.update_one(
            {"_id": post_id},
            {"$set": record}
        )
        print(f"{post_id} is already in our DB")

# Get:
db.facebook.find_one({"post_id": post_id})

# Delete collection:
db.facebook.drop_collection()