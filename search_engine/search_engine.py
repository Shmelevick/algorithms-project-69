import re

def search(docs: list, word: str) -> list:
    """
    Searches for a word in the documents and returns their IDs.
    """
    def preprocess(text):
        return re.sub(r'[^\w\s]', '', text).lower()
    
    result = []
    word = preprocess(word)
    for doc in docs:
        cleaned_text = preprocess(doc['text'])
        if word in cleaned_text.split():
            result.append(doc['id'])
    return result
