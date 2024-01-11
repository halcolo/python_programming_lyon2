import os
import re
import string
from typing import List
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

try:
    from nltk.corpus import stopwords
except ImportError:
    nltk.download('stopwords')
    from nltk.corpus import stopwords

from modules.auth import RedditAuth

        
def set_vars() -> RedditAuth:
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

    reddit_auth_setup = RedditAuth(
        client_secret=client_secret,
        user_agent=user_agent,
        client_id=client_id,
    )
    return reddit_auth_setup



def clean_paragraph(text: str) -> List[str]:
    """
    Cleans the given text by removing special characters, punctuation, and stopwords.

    Args:
        text (str): The text to be cleaned.

    Returns:
        List[str]: The cleaned text as list.
    """

    stopwords_set = set(stopwords.words('english'))
    
    # Separing, removing all special characters and not used words in tokenized text
    token = RegexpTokenizer(r'''\w'|\w+|[^\w\s]''')
    tokens = token.tokenize(text)
    tokens = [token for token in tokens if token not in string.punctuation]
    tokens = [token for token in tokens if token not in stopwords_set]
    tokens = [token for token in tokens if len(token) > 2]
    tokens = [token.translate(str.maketrans('', '', string.punctuation)).lower() for token in tokens]
    
    return tokens


def clean_text(text: str) -> str:
    """
    Clean the given text by removing square brackets and their contents,
    removing non-alphanumeric characters except for important symbols and spaces,
    and removing extra spaces.

    Args:
        text (str): The text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    text = re.sub(r'\[.*?\]', '', text)  # Remove square brackets and their contents
    text = re.sub(r"[^a-zA-Z0-9',?:!\s]", '', text)  # Remove non-alphanumeric characters
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    
    return text

def normalize_value(value: float, min_value: float, max_value: float) -> float:
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

def label_from_normalized_value(normalized_value: float) -> int:
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

