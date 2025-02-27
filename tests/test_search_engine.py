import pytest
from search_engine.search_engine import search

docs = [
    {'id': 1, 'text': 'hello world'},
    {'id': 2, 'text': 'hello, python'},
    {'id': 3, 'text': 'goodbye world!'},
    {'id': 4, 'text': 'hellothere'},
    {'id': 5, 'text': 'goodbye java'}
]


class TestSearchFunction:
    """
    Test the search function to ensure it handles various cases, including:
    - Finding words correctly.
    - Returning empty lists for absent words.
    - Not matching partial words.
    - Handling empty or whitespace-only search queries.
    """
    @pytest.mark.parametrize(
        'docs, word, res',
        [
            (docs, 'java', [5]),
            (docs, 'world', [1, 3]),
            (docs, 'hello', [1, 2]),
        ]
    )
    def test_search_single_word_found(self, docs, word, res):
        """
        Test the search function to ensure it finds a single word correctly.
        """
        assert search(docs, word) == res, f"Expected {res}, but got {search(docs, word)}"

    @pytest.mark.parametrize(
        'docs, word, res',
        [
            (docs, 'javascript', []),
            (docs, 'goodmorning', []),
            (docs, 'computer', []),
        ]
    )
    def test_search_absent_word_not_found(self, docs, word, res):
        """
        Test that the search function returns an empty list for absent words.
        """
        assert search(docs, word) == res, f"Expected [], but got {search(docs, word)}"

    @pytest.mark.parametrize(
        'docs, word, res',
        [
            (docs, 'he', []),
            (docs, 'hell', []),
            (docs, 'o', []),
        ]
    )
    def test_search_part_of_word_not_found(self, docs, word, res):
        """
        Test that the search function does not return results for partial words.
        """
        assert search(docs, word) == res, f"Expected [], but got {search(docs, word)}"

    @pytest.mark.parametrize('word', ['', ' ', '\t', '\n'])
    def test_search_empty_word(self, word):
        """
        Test that the search function returns an empty list for empty or whitespace-only queries.
        """
        assert search(docs, word) == [], f'Expected [], but got {search(docs, word)}'


    def test_with_punctuation(self):
        """
        Test that the search word can be with puntcuation
        """
        doc1 = {'id': 'doc1', 'text': "I can't shoot straight unless I've had a pint!"}
        docs = [doc1]

        assert search(docs, 'pint') == ['doc1']
        assert search(docs, 'pint!') == ['doc1']