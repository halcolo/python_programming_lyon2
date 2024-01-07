import os
from utils.tools import set_vars

CLIENT_SECRET = None
USER_AGENT = None
CLIENT_ID = None

if CLIENT_SECRET is not None and USER_AGENT is not None and CLIENT_ID is not None:
    os.environ["CLIENT_SECRET"] = CLIENT_SECRET 
    os.environ["USER_AGENT"] = USER_AGENT
    os.environ["CLIENT_ID"] =  CLIENT_ID

reddit_auth = set_vars()
