import pickle
import os
from modules.author import Author

class Corpus:
    """
    Class representing a corpus of documents.
    """
    _instance = None
    def __new__(cls, name:str='CORPUS'):
        """
        Initialize a Corpus object.
        
        Parameters:
            name (str): The name of the corpus.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.name = name
            # Author ID to Author mapping
            cls._instance.authors = dict()
            # ID to document mapping
            cls._instance.id2doc = dict()
            # Author to ID mapping
            cls._instance.aut2id = dict()
            # Number of documents
            cls._instance.ndoc = 0
            # Number of authors
            cls._instance.naut = 0
        return cls._instance

        
    def __repr__(self):
        """
        Return a string representation of the Corpus object.
        """
        docs = list(self._instance.id2doc.values())
        return "\n".join(list(map(str, docs)))

    def add(self, doc, author):
        """
        Add a document to the corpus.
        
        Parameters:
            doc: The document to add.
            author: The author of the document.
        """
        if author not in self._instance.aut2id:
            self._instance.naut += 1
            self._instance.authors[self._instance.naut] = Author(author)
            self._instance.aut2id[author] = self._instance.naut
        self._instance.authors[self._instance.aut2id[author]].add(doc.text)

        self._instance.ndoc += 1
        self._instance.id2doc[self._instance.ndoc] = doc
        
    def save_file(self, path: str, name: str = 'test'):
        """
        Save the corpus to a file.
        
        Parameters:
            path (str): The path to save the file.
            name (str): The name of the file. Default is 'test'.
        """
        data = list(self._instance.id2doc.values())

        # Export the list to a file
        with open(os.path.join(path, f'data_{name}.csv'), 'wb') as f:
            pickle.dump(data, f)
            
    def load_file(self, path: str):
        """
        Load a corpus from a file.
        
        Parameters:
            path (str): The path to the file.
        
        Returns:
            The loaded corpus.
        """
        with open(path, 'rb') as f:
            loaded_file = pickle.load(f)
        
        return loaded_file

    def show_metrics(self):
        """
        Display the metrics of the corpus.
        """
        # TODO: Implement the logic to calculate and display the metrics
        pass
        
    