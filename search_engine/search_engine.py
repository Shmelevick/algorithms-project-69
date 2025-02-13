import re

def search(docs: list, word: str) -> list:
    """
    Searches for a word in the documents and returns their IDs.
    """
    result = []
    word = word.lower()
    for doc in docs:
        cleaned_text = re.sub(r'[^\w\s]', '', doc['text'].lower())
        if word in cleaned_text.split():
            result.append(doc['id'])
    return result
