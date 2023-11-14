import logging
import os
import numpy as np
from modules.reddit_api import RedditApi
from modules.arxiv_api import ArxivApi
from modules.Corpus import Corpus


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
    

if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(path, 'data')
    arxiv_quantity = 100
    full_corpus = list()
    collection = []
    
    print('Reddit', '-'*20)
    print('GET REDDIT DATA')
    subreddit = 'MachineLearning'
    # subreddit = input('Which subreddit subject you want to get?: ')

    try:
        api_results = RedditApi(subreddit)
        docs = api_results.set_documents()
        collection += docs

    except TypeError as t:
        logging.error(t)
        raise TypeError
    except ValueError as v:
        logging.error(v)
        raise ValueError

    print('\nArxiv', '-'*20)
    print('GET ARXIV DATA')
    arxiv_kw = 'machine learning'
    # arxiv_kw = input('Which arxiv Keyword you want to get?: ')
    
    while arxiv_quantity > 100:
        arxiv_quantity = int(input('How many results you want? (max 100): '))

    try:
        arxiv_obj = ArxivApi(keyword=arxiv_kw, 
                             max_results=arxiv_quantity)
        
        data = arxiv_obj.get_data()
        collection += arxiv_obj.set_documents()
        
        full_corpus += arxiv_obj.set_documents()
    except TypeError as t:
        logging.error(t)
        raise TypeError
    except ValueError as v:
        logging.error(v)
        raise ValueError
    
    try:
        corpus = Corpus('Corpus_01')

        for doc in collection:
            for auth in doc.author:
                corpus.add(author=auth , doc=doc)
                
        # Save results
        corpus.save_file(data_path, 'new_file')
        data = corpus.load_file(os.path.join(data_path, 'data_new_file.csv'))

        # Show metrics using document generated
        show_metrics(data)
        
        
    except TypeError as t:
        logging.error(t)
        raise TypeError
    except ValueError as v:
        logging.error(v)
        raise ValueError
            
    
