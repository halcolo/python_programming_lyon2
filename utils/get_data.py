import requests
import xmltodict 
import praw
import logging
import pandas as pd
from utils.secrets import set_vars


def get_data(subreddit:str, 
             arxiv_kw:str, 
             csv_path:str, 
             limit:int=20) -> None:
    """
    Fetches data from Reddit and Arxiv API and saves it to a CSV file.

    Args:
        subreddit (str): The name of the subreddit to fetch data from.
        arxiv_kw (str): The keyword to search for in Arxiv API.
        csv_path (str): The path to save the CSV file.
        limit (int, optional): The maximum number of posts to fetch. Defaults to 20.
    """
    
    print('Reddit', '-'*20)
    print('GET REDDIT DATA')
    try:
        reddit_auth = set_vars()
        reddit = praw.Reddit(
                client_id=reddit_auth.client_id, 
                client_secret=reddit_auth.client_secret, 
                user_agent=reddit_auth.user_agent
            )
        
        data = reddit.subreddit(subreddit).hot(limit=limit)
        document = dict()
        document['docNum'] = list()
        document['text'] = list()
        document['origin'] = list()
        for doc in data:
            if doc.selftext == '':
                continue
            document['docNum'].append(len(document['docNum']))
            document['text'].append(str(doc.selftext).replace('\n', ' '))
            document['origin'].append('reddit')
        
    except TypeError as t:
        logging.error(t)
        raise TypeError
    except ValueError as v:
        logging.error(v)
        raise ValueError
    except AttributeError as v:
        logging.error(v)
        raise AttributeError

    
    print('\nArxiv', '-'*20)
    print('GET ARXIV DATA')
    arxiv_kw = 'machine learning'
    start = 0
    base_url = 'http://export.arxiv.org/api/query'
    query_params = {
            'search_query': f'all:{arxiv_kw}',
            'start': start,
            'max_results': limit
            }
    
    try:
        response = requests.get(url=base_url,
                                params=query_params)
        
        if response.status_code == 200:
            data = xmltodict.parse(response.content.decode())['feed']
            data = data['entry']
        else:
            raise ValueError
        
        for doc in data:
            if doc['summary'] == '':
                continue
            document['docNum'].append(len(document['docNum']))
            document['text'].append(str(doc['summary']).replace('\n',' '))
            document['origin'].append('arxiv')
            
    except TypeError as t:
        logging.error(t)
        raise TypeError
    except ValueError as v:
        logging.error(v)
        raise ValueError
    except AttributeError as v:
        logging.error(v)
        raise AttributeError
    
    # DF creation
    df = pd.DataFrame(document)

    # CSV creation
    df.to_csv(csv_path, index=False, sep='\t')
    

def data_manipulation(df:pd.DataFrame) -> None: 
    """
    Perform data manipulation on a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to be manipulated.

    Returns:
    None
    """
    print("DF length:", len(df))
    
    # Number of words by phrase
    for index, row in df.iterrows():
        text = row['text']
        words = text.split()
        print("Number of words in phrase", index+1, ":", len(words))
    
    # Delete texts less than 20 characters
    df = df[df['text'].str.len() >= 20]
    
    # Create unique string of characters
    all_texts = ''.join(df['text'])
    print("Unique string of characters:", all_texts)