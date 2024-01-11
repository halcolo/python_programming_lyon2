import os
import logging
import numpy as np
import pickle
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from utils.tools import clean_paragraph
from modules.corpus import Corpus
from modules.factory import DocumentFactory
from modules.document import Document



def search_documents(processes:list[dict]) -> Document:
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
    
    # pkl_file_name = f'corpus{datetime.datetime.now().strftime("%d%m%y")}{processes[0].get("topic")}.pkl'
    pkl_file_name = f'corpus_{processes[0].get("topic")}.pkl'
    pkl_file_path = 'data/' + pkl_file_name
    
    # Check if the pickle file exists to avoid recharacterizing the corpus
    if os.path.exists(pkl_file_path):
        with open(pkl_file_path, 'rb') as file:
            corpus = pickle.load(file)
        # logging.warn(f'Corpus loaded from {pkl_file_path}')
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
                document_collection = retrieved_documents.set_documents()
                
                corpus = Corpus()
                
                # Check if data is not empty
                if len(document_collection) == 0:
                    raise TypeError(f'No data provided by the API {process_type}')
                for i in range(len(document_collection)):
                    doc = document_collection[i]
                    author = doc.author if doc.author is not None else 'Anonymous'
                    corpus.add(author=author , doc=doc)
                    
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

def search_engine(collection:list, keywords:list):
    """
    Search engine function that takes a collection of documents and a list of keywords,
    and returns a sorted list of documents ids based on their similarity to the keywords 
    and a score this is a custom IT-IDF.

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
        
        words = clean_paragraph(doc.text)
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

