import os
from utils.tools import set_vars

img = {
    "reddit_logo": "https://github.com/jdalfons/search_engine/assets/25759070/0419f2e0-e103-4a57-9968-b4dcd56226b4",
    "arxiv_logo": "https://github.com/jdalfons/search_engine/assets/25759070/ae7e2ecf-1d4a-4779-a825-673bb2a83d6d",
}

CLIENT_SECRET = None
USER_AGENT = None
CLIENT_ID = None

if CLIENT_SECRET is not None and USER_AGENT is not None and CLIENT_ID is not None:
    os.environ["CLIENT_SECRET"] = CLIENT_SECRET 
    os.environ["USER_AGENT"] = USER_AGENT
    os.environ["CLIENT_ID"] =  CLIENT_ID

reddit_auth = set_vars()

