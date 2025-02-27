import re
from math import log2


def search(documents, query):
    inverted_index = get_inverted_index(documents)
    result_with_relevance = {}
    query_tokens = tokenize(query)
    for query_token in query_tokens:
        documents_has_token = inverted_index.get(query_token)
        if not documents_has_token:
            continue
        for document in documents_has_token:
            result_with_relevance.setdefault(document['id'], 0)
            token_tf_idf = get_tf_idf(document['id'], documents_has_token)
            result_with_relevance[document['id']] += token_tf_idf
    result = sorted(
        result_with_relevance,
        key=result_with_relevance.get,
        reverse=True)
    return result


def get_inverted_index(documents):
    inverted_index = {}
    tokens_all = set()
    documents_as_tokens = []
    for document in documents:
        document_tokens = tokenize(document['text'])
        current_document_tokenized = {
            'id': document['id'],
            'tokens': document_tokens
        }
        documents_as_tokens.append(current_document_tokenized)
        tokens_all.update(document_tokens)
    for token in tokens_all:
        inverted_index[token] = []
        idf = get_idf(documents_as_tokens, token)
        for document in documents_as_tokens:
            if token in document['tokens']:
                tf = get_tf(document['tokens'], token)
                current_document_with_relevance = {
                    'id': document['id'],
                    'tf-idf': round(tf * idf, 4)
                }
                inverted_index[token].append(current_document_with_relevance)
    return inverted_index


def tokenize(text):
    tokens = []
    text_lines = text.split('\n')
    for text_line in text_lines:
        text_line_tokenized = [
            get_term(token)
            for token in text_line.split(' ') if token
        ]
        tokens.extend(text_line_tokenized)
    return tokens


def get_term(token):
    return re.sub(r'[^\w\s]', '', token).lower()


def get_tf_idf(document_id, documents_has_token):
    filter_document_has_token = filter(
        lambda document: document['id'] == document_id, documents_has_token
    )
    document_has_token = list(filter_document_has_token)[0]
    tf_idf = document_has_token['tf-idf']
    return tf_idf


def get_tf(document_as_tokens, token):
    document_tokens_count = len(document_as_tokens)
    token_in_document_count = document_as_tokens.count(token)
    tf = token_in_document_count / document_tokens_count
    return tf


def get_idf(documents_as_tokens, token):
    documents_count = len(documents_as_tokens)
    filter_documents_has_token = filter(
        lambda document: token in document['tokens'], documents_as_tokens
    )
    documents_has_token = list(filter_documents_has_token)
    documents_has_token_count = len(documents_has_token)
    idf = log2((documents_count + 1) / (documents_has_token_count + 0.5))
    return idf
