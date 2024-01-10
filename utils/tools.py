import sys
import os
import re
import string
import numpy as np
from nltk.tokenize import RegexpTokenizer
import nltk


try:
    from nltk.corpus import stopwords
except ImportError:
    nltk.download('stopwords')
    from nltk.corpus import stopwords
from nltk.corpus import stopwords


class RedditAuth:
    """
    Class representing Reddit authentication credentials.
    """
    def __init__(self, client_secret: str, user_agent: str, client_id: str) -> None:
        """
        Initialize a RedditAuth object.
        
        Args::
            client_secret (str): The client secret.
            user_agent (str): The user agent.
            client_id (str): The client ID.
        """
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.client_id = client_id

def set_vars():
    """
    Set environment variables for Reddit authentication.

    This function get environment variables required for Reddit authentication. 
    Check `config.py` to set the user credentials for Reddit API.

    Returns:
        RedditAuth: An instance of the RedditAuth class with the client secret, user agent,
                    and client ID set.

    """

    client_secret = os.environ.get("CLIENT_SECRET")
    user_agent = os.environ.get("USER_AGENT")
    client_id = os.environ.get("CLIENT_ID")

    reddit_auth = RedditAuth(
        client_secret=client_secret,
        user_agent=user_agent,
        client_id=client_id,
    )
    return reddit_auth

def print_progress_bar(index, total, label):
    """
    Print a progress bar to the console.
    
    Args::
        index (int): The current index.
        total (int): The total number of iterations.
        label (str): The label to display.
    """
    n_bar = 50  # Progress bar width
    progress = index / total
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * progress):{n_bar}s}] {int(100 * progress)}%  {label}")
    sys.stdout.flush()



def clean_paragraph_util(text:str) -> list:
    """
    Cleans the given text by removing special characters, punctuation, and stopwords.

    Args:
        text (str): The text to be cleaned.

    Returns:
        list: The cleaned text as list.
    """

    stopwords_set = set(stopwords.words('english'))
    
    # Separing, removing all special characters and not used words in tokenized text
    token = RegexpTokenizer(r'''\w'|\w+|[^\w\s]''')
    tokens = token.tokenize(text)
    tokens = list(token for token in tokens if token not in string.punctuation)
    tokens = list(token for token in tokens if token not in stopwords_set)
    tokens = list(token for token in tokens if len(token) > 2)
    tokens = list(token.translate(str.maketrans('', '', string.punctuation)).lower() for token in tokens)
    
    return tokens


def clean_text(text):
    """
    Clean the given text by removing square brackets and their contents,
    removing non-alphanumeric characters except for important symbols and spaces,
    and removing extra spaces.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r"[^a-zA-Z0-9',?:!\s]", '', text)
    text = ' '.join(text.split())
    
    return text

def normalize_value(value, min_value, max_value):
    """
    Normalize a value between 0 and 1 based on the given minimum and maximum values.

    Args:
        value (float): The value to be normalized.
        min_value (float): The minimum value of the range.
        max_value (float): The maximum value of the range.

    Returns:
        float: The normalized value between 0 and 1.
    """
    if min_value == max_value:
        return 0.5  
    return (value - min_value) / (max_value - min_value)

def label_from_normalized_value(normalized_value):
    """
    Assigns a label based on the given normalized value.
    
    0 - 0.3: Low similarity
    0.3 - 0.6: Medium similarity
    0.6 - 0.8: High similarity
    0.8 - 1: Very high similarity

    Args:
        normalized_value (float): The normalized value to assign a label to.

    Returns:
        int: The label assigned to the normalized value.
    """
    if normalized_value < 0.3:
        return 0
    elif 0.4 <= normalized_value < 0.7:
        return 1
    else:
        return 2
    
class SingletonMeta(type):
    """
    Metaclass for implementing the Singleton design pattern.

    This metaclass ensures that only one instance of a class is created and
    provides a global point of access to that instance.

    Usage:
    class MyClass(metaclass=SingletonMeta):
        # class definition

    Note:
    This metaclass should be used as the metaclass of the class that needs to
    be a singleton.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
