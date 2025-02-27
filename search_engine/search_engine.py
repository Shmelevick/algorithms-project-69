import re
from collections import defaultdict


def search(docs: list, words: str) -> list:
    """
    Searches for words in the documents and returns their IDs,
    ranked by the total count of word occurrences in the document text.
    """
    def preprocess(text):
        return re.sub(r'[^\w\s]', '', text).lower()

    result = []
    words = preprocess(words).split()


    for doc in docs:
        cleaned_text = preprocess(doc['text'])
        word_count = 0

        for word in words:
            word_count += cleaned_text.split().count(word)

        if word_count:
            result.append({
                'id': doc['id'],
                'word_count': word_count
            })

    result.sort(key=lambda x: x['word_count'], reverse=True)

    return [item['id'] for item in result]
