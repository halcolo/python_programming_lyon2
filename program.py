import logging
import config   
import pandas as pd
import numpy as np
from modules.corpus import Corpus
from utils.tools import clean_text_util
from scipy.sparse import csr_matrix
from modules.factory import DocumentFactory
from sklearn.metrics.pairwise import cosine_similarity


    
def setup_process(type:str, key_word:str, quantity:int=10):
    try:
        args = {
            "type_process": type,
            "keyword": key_word,
            "max_results": quantity
        }

        api_results = DocumentFactory(data=args).create_document()
        
        # Check if data is not empty
        if api_results is None:
            raise ValueError('No data provided check your credentials')
        
        return api_results.set_documents()

    except TypeError as t:
        logging.error(t)
        raise TypeError
    except ValueError as v:
        logging.error(v)
        raise ValueError


def search_engine(collection, keywords:list):
    
    # Create a dict to store corpus vocabulary
    # Getting Vocabulary
    new_collection = dict()
    vocab = list()
    
    for i, doc in enumerate(collection):
        
        new_collection[i] = dict()
        
        words = clean_text_util(doc.text)
        unique_words = set(words)
        vocab += unique_words
        word_counts = dict()
        
        for word in unique_words:
            word_counts[word] = words.count(word)
            
        new_collection[i] = dict((('doc', doc), ('word_counts', word_counts)))
    
    vocab = list(set(vocab))
    
    mat_tf = csr_matrix((len(collection), len(vocab)), dtype=int).toarray()

    for i, doc in new_collection.items():
        for j, word in enumerate(vocab):
            if word in doc['word_counts'].keys():
                mat_tf[i, j] += doc['word_counts'][word]
                
    query_vector = np.zeros((1, len(vocab)))

    # Set the weights of the query vector based on the importance of the keywords
    for i, word in enumerate(vocab):
        if word in keywords:
            query_vector[0, i] = 1  # Set the weight to 1 if the word is in the keywords

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(query_vector, mat_tf)

    # Get indices of articles with highest similarity scores
    top_articles_indices = np.argsort(similarity_scores)[0][::-1]

    # Create a list to store the results
    results = []

    # Store the document URL, similarity score, and document text in a dictionary
    for i in top_articles_indices:
        result = {
            'Document URL': collection[i].url,
            'Similarity Score': similarity_scores[0, i],
            'Document Text': collection[i].text
        }
        results.append(result)

    # Return sorted the results by similarity score in descending order
    return sorted(results, key=lambda x: x['Similarity Score'], reverse=True)


def full_search_engine_proc(arxiv_kw:str, subreddit_kw:str) -> list:
    collection = list()
    print("starting process")
    
    collection += setup_process(
        type='reddit', 
        key_word=subreddit_kw
    )
    
    collection += setup_process(
        type='arxiv', 
        key_word=arxiv_kw
    )
    
    return collection