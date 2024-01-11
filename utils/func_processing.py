import logging
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def calculate_similarity_articles(df):
    """
    Calculate the cosine similarity between articles in a DataFrame using sklearn library.

    Args:
        df (pd.DataFrame): DataFrame containing articles with 'source', 'id', 'title', and 'text' columns.

    Returns:
        pd.DataFrame: DataFrame containing the cosine similarity scores between articles.
    """
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
    except TypeError as e:
        logging.error(e)
        raise TypeError
    except ValueError as e:
        logging.error(e)
        raise ValueError




def process_similarity_pairs(df_corpus, similarity_df):
    """
    Process similarity pairs based on the given dataframe corpus and similarity dataframe.

    Args:
        df_corpus (pandas.DataFrame): The dataframe corpus containing unique IDs.
        similarity_df (pandas.DataFrame): The similarity dataframe.

    Returns:
        dict: A dictionary containing similarity pairs categorized by source and ID.
            The structure of the dictionary is as follows:
            {
                'reddit': {
                    'source_id': [
                        {
                            'similar_source': 'similar_source',
                            'similar_id': 'similar_id',
                            'similarity': similarity_value
                        },
                        ...
                    ],
                    ...
                },
                'arxiv': {
                    'source_id': [
                        {
                            'similar_source': 'similar_source',
                            'similar_id': 'similar_id',
                            'similarity': similarity_value
                        },
                        ...
                    ],
                    ...
                }
            }
    """
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