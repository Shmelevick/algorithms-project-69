import re

def search(docs, word):
    result = []
    word = word.lower()
    for doc in docs:
        cleaned_text = re.sub(r'[^\w\s]', '', doc['text'].lower())
        if word in cleaned_text.split():
            result.append(doc['id'])
    return result
