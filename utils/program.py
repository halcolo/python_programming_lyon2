import os
import datetime
import logging
import config   
import pandas as pd
import numpy as np
import pickle
from collections import defaultdict
from modules.corpus import Corpus
from utils.tools import clean_paragraph_util
from scipy.sparse import csr_matrix
from modules.factory import DocumentFactory
from modules.document import ArxivDocument, RedditDocument
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def calculate_similarity_articles(df):

    try:
        df['unique_id'] = df['source'] + '_' + df['id'].astype(str)
        df['text_corpus'] = df['title'] + ' ' + df['text'] 
        # Create and apply TF-IDF vectorizer to texts
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(df['text_corpus'])

        # cosine similarity for all texts in corpus
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

        similarity_df = pd.DataFrame(cosine_similarities, index=df['unique_id'], columns=df['unique_id'])
        
        return similarity_df
    except Exception as e:
        logging.error(e)
        raise ValueError


def search_documents(processes: list):
    """
    Search documents based on the given processes.
    
    Args:
        processes (list): A list of dictionaries containing the process details.
            Each dictionary should have the following keys:
            - type (str): The type of process to be performed.
            - keyword (str): The keyword to search for.
            - quantity (int, optional): The maximum number of results to retrieve. Defaults to 10.

            Example:
            processes = [
                {'type':'reddit', 'keyword':'MachineLearning'},
                {'type':'arxiv', 'keyword':'machine learning'}
            ]

    Returns:
        api_results (Document): The retrieved documents.

    Raises:
        ValueError: If no data is provided or if the credentials are incorrect.
        TypeError: If there is a type error.
    """
    
    pkl_file_name = f'corpus{datetime.datetime.now().strftime("%d%m%y")}{processes[0].get("topic")}.pkl'
    pkl_file_path = 'data/' + pkl_file_name
    
    # Check if the pickle file exists to avoid recharacterizing the corpus
    if os.path.exists(pkl_file_path):
        with open(pkl_file_path, 'rb') as file:
            corpus = pickle.load(file)
        logging.warn(f'Corpus loaded from {pkl_file_path}')
    else:
        try:
            for process in processes:
                if process.get("type") is None or process.get("keyword") is None:
                    raise TypeError('Missing arguments')
                process_type = process.get("type")
                keyword = process.get("keyword")
                quantity = process.get("quantity", 10)
                
                args = {
                    "type_process": process_type,
                    "keyword": keyword,
                    "max_results": quantity
                }
                retrieved_documents = DocumentFactory(data=args).create_document()
                print('source', process_type)
                document_collection = retrieved_documents.set_documents()
                print('retrieved_documents', len(document_collection))
                
                corpus = Corpus()
                
                # Check if data is not empty
                if len(document_collection) == 0:
                    raise TypeError(f'No data provided by the API {process_type}')
                for i in range(len(document_collection)):
                    doc = document_collection[i]
                    corpus.add(author=doc.author , doc=doc)
                    
        except TypeError as t:
            logging.error(t)
            raise TypeError
        except ValueError as v:
            logging.error(v)
            raise ValueError
    # Save the corpus to a pickle file
    with open(pkl_file_path, 'wb') as file:
        pickle.dump(corpus, file, fix_imports=False)
    return corpus


## DEPRECATED
def full_search_engine_proc(arxiv_kw:str, subreddit_kw:str) -> list:
    """
    Perform a full search engine process by searching for keywords in both Reddit and Arxiv.

    Args:
        arxiv_kw (str): The keyword to search for in Arxiv.
        subreddit_kw (str): The keyword to search for in Reddit.

    Returns:
        list: A collection of search results from both Reddit and Arxiv.
    """

    documents = [
        {'type':'reddit', 'keyword':subreddit_kw},
        {'type':'arxiv', 'keyword':arxiv_kw}
    ]


    corpus = search_documents(documents)

    
    
    return corpus


# DEPRECATED
def words_it_idf(collection:list) -> dict:
    """
    Calculate the inverse document frequency of each word in the corpus.
    
    Args:
        collection (list): A list of documents in the corpus.
    
    Returns:
        dict: A dictionary of words and their corresponding IDF values.
    """
    # Create a dict to store corpus vocabulary
    vocab = dict()
    # Create a dict to store the IDF values
    idf = dict()
    
    for i, doc in enumerate(collection):
        words = clean_paragraph_util(doc.text)
        unique_words = set(words)
        for word in unique_words:
            if word in vocab.keys():
                vocab[word] += 1
            else:
                vocab[word] = 1
    
    # cosine_similarity(collection, vocab)
    for word in vocab.keys():
        idf[word] = np.log(len(collection) / vocab[word])
    
    return idf

def search_engine(collection:list, keywords:list):
    """
    Search engine function that takes a collection of documents and a list of keywords,
    and returns a sorted list of documents ids based on their similarity to the keywords 
    and a score.

    Args::
        collection (list): A list of documents.
        keywords (list): A list of keywords.

    Returns:
        list: A sorted list of dictionaries containing the document URL, similarity score,
              and document text.
    """
    
    # Rest of the code...
    
    # Create a dict to store corpus vocabulary
    # Getting Vocabulary
    new_collection = dict()
    vocab = list()
    
    for i, doc in enumerate(collection):
        
        new_collection[i] = dict()
        
        words = clean_paragraph_util(doc.text)
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
            'id': i,
            'source': collection[i].source,
            'score': similarity_scores[0, i],
        }
        results.append(result)

    # sort results and filter out results with 0 similarity score
    sorted_scores = sorted(results, key=lambda x: x['score'], reverse=True)
    filtered_results = list(filter(lambda x: x['score'] > 0, sorted_scores))
    

    return filtered_results


def calculate_word_freq_per_year(corpus, words_to_track):
    word_freq_per_year = defaultdict(lambda: defaultdict(int))
    
    for doc in list(corpus.documents.values()):
        try:
            date = doc.date
            year = date.year
        except ValueError:
            continue
        for word in words_to_track:
            word_freq = doc.text.lower().count(word.lower())
            key = (word, str(year))
            word_freq_per_year[key] = word_freq
    
    return word_freq_per_year


def process_similarity_pairs(df_corpus, similarity_df):
    similarity_pairs = {'reddit': {}, 'arxiv': {}}
    
    for idx in df_corpus['unique_id'].tolist():
        similarity_pairs[idx.split('_')[0]][idx.split('_')[1]] = []
        selected_rows = similarity_df.loc[df_corpus['unique_id'], idx]
        selected_df = selected_rows.reset_index()
        selected_df_sorted = selected_df.sort_values(by=idx, ascending=False)
        selected_df_sorted = selected_df_sorted.drop(selected_df_sorted[selected_df_sorted['unique_id'] == idx].index)
        selected_df_sorted = selected_df_sorted.drop(selected_df_sorted[selected_df_sorted[idx] <= float(0.0)].index)
        
        if len(selected_df_sorted) > 0:
            selected_df_filtered = selected_df_sorted.tail(3)
            
            for i in selected_df_filtered['unique_id'].tolist():
                similarity_pairs[idx.split('_')[0]][idx.split('_')[1]].append({
                    'similar_source': i.split('_')[0],
                    'similar_id': i.split('_')[1],
                    'similarity': selected_df_filtered[selected_df_filtered['unique_id'] == i][idx].values[0]
                })
    
    return similarity_pairs