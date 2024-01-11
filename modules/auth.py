class RedditAuth:
    """
    Class representing Reddit authentication credentials.
    """
    def __init__(self, client_secret: str, user_agent: str, client_id: str) -> None:
        """
        Initialize a RedditAuth object.
        
        Args:
            client_secret (str): The client secret.
            user_agent (str): The user agent.
            client_id (str): The client ID.
        """
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.client_id = client_id