import os
import subprocess

class RedditAuth:
    """
    Class representing Reddit authentication credentials.
    """
    def __init__(self, client_secret: str, user_agent: str, client_id: str) -> None:
        """
        Initialize a RedditAuth object.
        
        Parameters:
            client_secret (str): The client secret.
            user_agent (str): The user agent.
            client_id (str): The client ID.
        """
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.client_id = client_id

def set_vars():
    # Run the shell script file with secrets
    path = os.path.dirname(os.path.realpath(__file__))
    secrets_path = os.path.join(path, 'secrets.sh')
    subprocess.run(["sh", secrets_path])

    client_secret = os.environ.get("CLIENT_SECRET")
    user_agent = os.environ.get("USER_AGENT")
    client_id = os.environ.get("CLIENT_ID")

    reddit_auth = RedditAuth(
        client_secret=client_secret,
        user_agent=user_agent,
        client_id=client_id,
    )
    return reddit_auth
