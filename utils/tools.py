import sys
import os
import string
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import string




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


def show_metrics(full_corpus):
    """
    Prints various metrics about the given corpus.
    
    Parameters:
        full_corpus (list): A list of documents in the corpus.
    """
    print('Data manipulation', '-'*20)
    print('Corpus Length:', len(full_corpus))
    
    words = [len(doc.text.split(' ')) for doc in full_corpus]
    phrases = [len(doc.text.split('.')) for doc in full_corpus]
    
    print('Number of words:', str(np.mean(words)))
    print('Average phrases:', str(np.mean(phrases)))
    print('Total words:', str(np.sum(words)))
    
    long_docs = [doc.text for doc in full_corpus if len(doc.text) > 20]
    
    print('Total long docs:', len(long_docs))
    
    full_string = ' '.join([doc.text for doc in full_corpus])
    # print(full_string)


def print_progress_bar(index, total, label):
    """
    Print a progress bar to the console.
    
    Parameters:
        index (int): The current index.
        total (int): The total number of iterations.
        label (str): The label to display.
    """
    n_bar = 50  # Progress bar width
    progress = index / total
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'=' * int(n_bar * progress):{n_bar}s}] {int(100 * progress)}%  {label}")
    sys.stdout.flush()



def clean_text_util(text:str) -> list:
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


def singleton(class_):
    instance = None
    def getinstance(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = class_(*args, **kwargs)
        return instance
    def deleteinstance():
        nonlocal instance
        if instance is not None:
            del instance
            instance = None
    getinstance.delete = deleteinstance
    return getinstance
