import pickle
import os
from modules.Author import Author

class Corpus:
    """
    Class representing a corpus of documents.
    """
    def __init__(self, name: str) -> None:
        """
        Initialize a Corpus object.
        
        Parameters:
            name (str): The name of the corpus.
        """
        self.name = name
        self.authors = dict()
        self.id2doc = dict()
        self.aut2id = dict()
        self.ndoc = 0
        self.naut = 0
        
    def __repr__(self):
        """
        Return a string representation of the Corpus object.
        """
        docs = list(self.id2doc.values())
        return "\n".join(list(map(str, docs)))

    def add(self, doc, author):
        """
        Add a document to the corpus.
        
        Parameters:
            doc: The document to add.
            author: The author of the document.
        """
        if author not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(author)
            self.aut2id[author] = self.naut
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
        data = list(self.id2doc.values())

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

    