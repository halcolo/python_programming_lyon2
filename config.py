import os
from utils.secrets import set_vars

# CHANGE THIS BY YOUR OWN CREDENTIALS
os.environ["CLIENT_SECRET"] = "REPLACE_ME"
os.environ["USER_AGENT"] = "REPLACE_ME"
os.environ["CLIENT_ID"] = "REPLACE_ME"

reddit_auth = set_vars()