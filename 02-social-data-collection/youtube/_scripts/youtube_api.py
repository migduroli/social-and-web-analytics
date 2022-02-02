import json
import googleapiclient.discovery

# API information
api_service_name = "youtube"
api_version = "v3"

# API key
with open("auth/youtube_credentials.json") as file:
    credentials = json.load(file)

DEVELOPER_KEY = credentials["DEVELOPER_KEY"]


# API client
youtube = googleapiclient.discovery.build(
    serviceName=api_service_name,
    version=api_version,
    developerKey=DEVELOPER_KEY
)

# Request body:
request = youtube.search().list(
    part="id,snippet",
    type='video',
    q="Spider-Man",
    videoDuration='short',
    videoDefinition='high',
    maxResults=10
)

# Request execution:
response = request.execute()
print(response)


# Video by ID:
video_id = "jg0H9uvZa-c"

request = youtube.videos().list(
    part="contentDetails,id,liveStreamingDetails,localizations,player,"
         "recordingDetails,snippet,statistics,status,"
         "topicDetails",
    id=video_id
).execute()

# Comments in video:
token = None
comments = []
for i in range(1,8):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        order="relevance",
        pageToken=token,
        maxResults=100,
    ).execute()
    token = request["nextPageToken"]
    comments += request["items"]

request = youtube.channels().list(
    part="id,snippet,statistics",
    forUsername="elrubiusOMG"
).execute()


YOUTUBERS = [
    "elrubiusOMG",
    "VEGETTA777",
    "Mikecrack",
    "AuronPlay",
    "TheWillyRex",
    "Makiman131",
]

channel_data = []
for user_name in YOUTUBERS:
    try:
        data = youtube.channels().list(
            part="id,snippet,statistics",
            forUsername=user_name,
        ).execute()["items"]
        channel_data += data
        print(f"user: {user_name} => subscribers: {data[0]['statistics']['subscriberCount']}")
    except:
        print(f"No data found: {user_name}")
