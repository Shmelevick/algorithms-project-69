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
        word_count = cleaned_text.split().count(word)

        if word_count:
            result.append((doc['id'], word_count))

    result.sort(key=lambda x: x[1], reverse=True)
    return [id for id, _ in result]
