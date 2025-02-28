import re
import math


def compare_by_if_idf(item1, item2):
    if item1['TFIDF'] < item2['TFIDF']:
        return -1
    elif item1['TFIDF'] == item2['TFIDF']:
        return 0
    else:
        return 1


def quickSort(items, comparator, direction='asc'):
    items_length = len(items)

    if items_length == 0:
        return []

    index = items_length // 2
    element = items[index]

    smaller_items = [
        items[i]
        for i in range(items_length)
        if comparator(items[i], element) < 0 and i != index
    ]

    bigger_items = [
        items[i]
        for i in range(items_length)
        if comparator(items[i], element) >= 0 and i != index
    ]

    sorted_smaller_items = quickSort(smaller_items, comparator, direction)
    sorted_bigger_items = quickSort(bigger_items, comparator, direction)

    if direction == 'asc':
        return [*sorted_smaller_items, element, *sorted_bigger_items]
    return [*sorted_bigger_items, element, *sorted_smaller_items]


def get_index(docs):
    index = {}
    docs_count = len(docs)
    for doc in docs:
        temp_dict = {}
        number_words = 0
        for token in doc['text'].split():
            term = re.findall(r'\w+', token)
            index_key = ''.join(term).lower()
            if index_key not in temp_dict:
                temp_dict[index_key] = 0
            temp_dict[index_key] += 1
            number_words += 1
        for key, TF in temp_dict.items():
            if key not in index:
                index[key] = [{'id': doc['id'], 'TF': TF / number_words}]
            else:
                index[key].append({'id': doc['id'], 'TF': TF / number_words})
    for key, list_doc in index.items():
        docs_with_term = len(list_doc)
#        IDF = math.log10( docs_count / docs_with_term )
# Math.log2(1 + (docsCount - termCount + 1) / (termCount + 0.5));
# docsCount - общее количество документов
# termCount - количество документов, в которых встречается искомое слово
# Это несколько "сглаженный" вариант основной формулы
# линтер требует одновременно соблюдать W503 и W504
        part_idf = (docs_count - docs_with_term + 1) / (docs_with_term + 0.5)
        IDF = math.log2(1 + part_idf)
        for doc in list_doc:
            doc['TFIDF'] = doc['TF'] * IDF
    return index


def search(docs: dict, search_pattern: str):
    keys = []
    index = get_index(docs)
    search_results = {}
    search_worlds = search_pattern.split()
    for search_world in search_worlds:
        term = re.findall(r'\w+', search_world)
        search_world_lower = ''.join(term).lower()
        if search_world_lower in index:
            for doc in index[search_world_lower]:
                if doc['id'] not in search_results:
                    search_results[doc['id']] = doc['TFIDF']
                else:
                    search_results[doc['id']] += doc['TFIDF']
    search_results_list = []
    for doc, TFIDF in search_results.items():
        search_results_list.append({'id': doc, 'TFIDF': TFIDF})
    search_results = quickSort(search_results_list,
                               compare_by_if_idf,
                               'desc')
    print(search_results)
    for result in search_results:
        keys.append(result['id'])
    return keys
