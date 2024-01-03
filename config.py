import os
from utils.secrets import set_vars

# CHANGE THIS BY YOUR OWN CREDENTIALS
# os.environ["CLIENT_SECRET"] = "REPLACE_ME"
# os.environ["USER_AGENT"] = "REPLACE_ME"
# os.environ["CLIENT_ID"] = "REPLACE_ME"

os.environ["CLIENT_SECRET"] = "g8rgC38cYd2-CssRhI654dxlHjTUrw"
os.environ["USER_AGENT"] = "test_python_bot"
os.environ["CLIENT_ID"] = "itnNCnpIdc9GvcJ0wDm6fg"

reddit_auth = set_vars()