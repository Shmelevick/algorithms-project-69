import pytest
from search_engine.search_engine import search

docs = [
    {'id': 1, 'text': 'hello world'},
    {'id': 2, 'text': 'hello, python'},
    {'id': 3, 'text': 'goodbye world!'},
    {'id': 4, 'text': 'hellothere'},
    {'id': 5, 'text': 'goodbye java'}
]

def test_search_single_word_found():
    result = search(docs, 'java')
    assert result == [5], f"Expected [5], but got {result}"

def test_search_single_words_found_2():
    result = search(docs, 'hello')
    assert result == [1, 2], f"Expected [1, 2], but got {result}"

def test_search_absent_word_not_found():
    result = search(docs, 'goodmorning')
    assert result == [], f"Expected [], but got {result}"

def test_search_part_of_word_not_found():
    result = search(docs, 'he')
    assert result == [], f"Expected [], but got {result}"

def test_search_with_multiple_words_in_text():
    result = search(docs, 'world')
    assert result == [1, 3], f"Expected [1, 3], but got {result}"

def test_search_empty_word():
    result = search(docs, '')
    assert result == [], f"Expected [], but got {result}"
