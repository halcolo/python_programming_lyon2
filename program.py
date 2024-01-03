import logging
import config   
from modules.factory import DocumentFactory
    
def setup_process(type:str, key_word:str, quantity:int=100):
    print('Reddit', '-'*20)
    print(f'GETTING {type.upper()} DATA')
    try:
        args = {
            "type_process": type,
            "keyword": key_word,
            "max_results": quantity
        }

        api_results = DocumentFactory(data=args).create_document()
        
        # Check if data is not empty
        if api_results is None:
            raise ValueError('No data provided')
        
        return api_results.set_documents()

    except TypeError as t:
        logging.error(t)
        raise TypeError
    except ValueError as v:
        logging.error(v)
        raise ValueError


    