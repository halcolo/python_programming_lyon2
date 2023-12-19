import os
import config
import pandas as pd
from utils.get_data import (
    get_data,
    data_manipulation)
    
if __name__ == '__main__':
    subreddit = 'MachineLearning'
    arxiv_kw = 'machine learning'
    
    path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(path, 'data')
    
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Check if document.csv exists
    csv_path = os.path.join(data_path, 'document.csv')
    if not(os.path.exists(csv_path)):
        get_data(subreddit, arxiv_kw, csv_path)
        
    df = pd.read_csv(csv_path, sep='\t')

    # Data manipulation of df
    data_manipulation(df)

    
        
