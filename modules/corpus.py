import _pickle as cpickle
import os
import re
from utils.tools import singleton
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem.wordnet import WordNetLemmatizer
import numpy as np
import pandas as pd
from modules.author import Author


@singleton
class Corpus:
    """
    Class representing a corpus of documents.
    """
    __concated_text = None

    def __init__(self, name:str='Corpus 1'):
        """
        Initialize a Corpus object.
        
        Parameters:
            name (str): The name of the corpus.
        """
        self.name = name
        # Author ID to Author mapping
        self.authors = dict()
        # ID to document mapping
        self.id2doc = dict()
        # Author to ID mapping
        self.aut2id = dict()
        # Number of documents
        self.ndoc = 0
        # Number of authors
        self.author_num = 0

    def __repr__(self):
        """
        Returns:
            String representation of the Corpus object.
        """
        docs = list(self.id2doc.values())
        return "\n".join(list(map(str, docs)))

    def __str__(self):
        return str(self.id2doc)
    
    def add(self, doc, author):
        """
        Add a document to the corpus.
        
        Parameters:
            doc: The document to add.
            author: The author of the document.
        """
        if author not in self.aut2id:
            self.author_num += 1
            self.authors[self.author_num] = Author(author)
            self.aut2id[author] = self.author_num
        self.authors[self.aut2id[author]].add(doc.text)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    def save_file(self, path: str, name: str = 'test'):
        """
        Save the corpus to a file.
        
        Parameters:
            path (str): The path to save the file.
            name (str): The name of the file. Default is 'test'.
        """
        data = self

        # Export the list to a file

        with open(os.path.join(path, f'data_{name}.pickle'), 'wb') as f:
            cpickle.dump(data, f)

    def load_file(self, path: str):
        """
        Load a corpus from a file.
        
        Parameters:
            path (str): The path to the file.
        
        Returns:
            The loaded corpus.
        """
        with open(path, 'rb') as f:
            loaded_file = cpickle.load(f)

        return loaded_file
    
        
    def corpus_stats(self) -> None:
        """
        Calculates and prints following statistics about the corpus.

        - Corpus Length: The total number of documents in the corpus.
        - Number of words: The average number of words per document.
        - Average phrases: The average number of phrases per document.
        - Total words: The total number of words in the corpus.
        - Total long docs: The number of documents with more than 20 characters.

        """
        full_corpus = self.id2doc.values()
        print('Data manipulation', '-'*20)
        print('Corpus Length:', len(full_corpus))
        
        words = [len(doc.text.split(' ')) for doc in full_corpus]
        phrases = [len(doc.text.split('.')) for doc in full_corpus]
        
        print('Number of words:', str(np.mean(words)))
        print('Average phrases:', str(np.mean(phrases)))
        print('Total words:', str(np.sum(words)))
        
        long_docs = [doc.text for doc in full_corpus if len(doc.text) > 20]
        
        print('Total long docs:', len(long_docs))
    
    def concat_data(self) -> None:
        """
        Concatenate all documents in the corpus if not concated.
        """
        if self.__concated_text is None:
            self.__concated_text = "".join([doc.text for doc in self.id2doc.values()])
        
    def search(self, keyword:str) -> re.Match:
            """
            Search for passages in the documents containing the given keyword.
            
            Parameters:
                keyword (str): The keyword to search for.
            
            Returns:
                re.Match: A match object containing the matched passages.
            """
            self.concat_data()
            
            match = re.finditer(keyword, self.__concated_text)
            return match

    def concorde(self, keyword:str, context_size:int=10) -> pd.DataFrame:
        """
        Build a concordance for the given expression.
        
        Parameters:
            keyword (str): The keyword to search for.
            context_size (int): The size of the context.
        
        Returns:
            A pandas DataFrame containing the concordance.
        """
        matches = self.search(keyword)
        concordance = []
        
        for match in matches:
            start = max(0, match.start() - context_size)
            end = min(len(self.__concated_text), match.end() + context_size)
            context_left = self.__concated_text[start:match.start()]
            context_right = self.__concated_text[match.end():end]
            if (context_left, match.group(), context_right) not in concordance:
                concordance.append((context_left, match.group(), context_right))
        
        df = pd.DataFrame(concordance, columns=['Context Left','Expression', 'Context Right'])
        return df

    def clean_text(self, doc:str=None) -> None:
        
        from utils.tools import clean_text_util
        
        if doc is None:
            self.concat_data()
            cleaned_doc = self.__concated_text

        else: cleaned_doc = doc
        
        words = clean_text_util(cleaned_doc)
        cleaned_doc = ' '.join(words)
        
        return cleaned_doc
        
        
        
    def stats(self) -> pd.DataFrame:
        cleaned_doc = self.clean_text()
        words = list()
        count = list()
        counter_docs = list()
        splited_text = list()
        ids = list()
        counter = 0
        for doc in self.id2doc:
            splited_text.append(self.clean_text(self.id2doc[doc].text).split(' '))
        
        splited_text.sort()  # Sort the splited_text list alphabetically
        
        for word in set(cleaned_doc.split(' ')):
            counter += 1
            ids.append(counter)
            words.append(word)
            count.append(cleaned_doc.count(word))
            counter_docs.append(sum([1 for doc in splited_text if word in doc]))
        
        data = {'id': ids, 'word': words, 'count': count, 'counter_docs': counter_docs}
        
        df = pd.DataFrame(data)
        
        return df
    
    def get_docs_by_author(self, author: str) -> list:
        """
        Get all documents of the given author.
        
        Parameters:
            author (str): The author to get the documents of.
        
        Returns:
            A list of documents.
        """
        return self.authors[self.aut2id[author]].docs
    
    def get_all_docs(self) -> list:
        """
        Get all documents in the corpus.
        
        Returns:
            A list of documents.
        """
        return list(self.id2doc.values())
        
                
        
        
        
        
        
