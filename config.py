import os
from utils.tools import set_vars

os.environ["CLIENT_SECRET"] = "CHANGE_ME"
os.environ["USER_AGENT"] = "CHANGE_ME"
os.environ["CLIENT_ID"] = "CHANGE_ME"


reddit_auth = set_vars()
