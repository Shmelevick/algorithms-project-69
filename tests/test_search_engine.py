import pytest
from search_engine.search_engine import search, get_inverted_index

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
        result = search(docs, word)
        assert result == res, f"Expected {res}, but got {result}"

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
        assert search(docs, word) == res, f"""Expected [], but got {
            search(docs, word)
        }"""

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
        Test that the search function does not return
        results for partial words.
        """
        assert search(docs, word) == res, f"Expected [], but got {
            search(docs, word)
        }"

    @pytest.mark.parametrize('word', ['', ' ', '\t', '\n'])
    def test_search_empty_word(self, word):
        """
        Test that the search function returns an empty list for empty
        or whitespace-only queries.
        """
        assert search(docs, word) == [], f'''Expected [], but got {
            search(docs, word)
        }'''


    def test_search_word_with_punctuation(self):
        """
        Test that the search word can be with puntcuation
        """
        doc1 = {
            'id': 'doc1',
            'text': "I can't shoot straight unless I've had a pint!"
        }
        docs = [doc1]

        assert search(docs, 'pint') == ['doc1']
        assert search(docs, 'pint!') == ['doc1']
        
    def test_search_ranging(self):
        """
        Test that the search function returns results
        sorted by the frequency of the search word's occurrence
        in the document text.
        """
        doc1 = "I can't shoot straight unless I've had a pint!"
        doc2 = "Don't shoot shoot shoot that thing at me."
        doc3 = "I'm your shooter."

        docs = [
            {'id': 'doc1', 'text': doc1},
            {'id': 'doc2', 'text': doc2},
            {'id': 'doc3', 'text': doc3},
        ]

        result = search(docs, 'shoot')
        assert result == ['doc2', 'doc1']

    def test_search_multiple_words(self):
        """
        Test that the search function returns documents
        containing all the words in the search query, and
        sorts them based on the frequency of the words' occurrence.

        The test ensures the following:
        - The search can handle multiple words (i.e., 'shoot at me').
        - Documents are returned in the order of their relevance 
        (based on word frequency).
        - Words in the search query are treated independently 
        (i.e., not as a single phrase).
        """
        doc1 = "I can't shoot straight unless I've had a pint!"
        doc2 = "Don't shoot shoot shoot that thing at me."
        doc3 = "I'm your shooter."

        docs = [
            {'id': 'doc1', 'text': doc1},
            {'id': 'doc2', 'text': doc2},
            {'id': 'doc3', 'text': doc3},
        ]

        result = search(docs, 'shoot at me')
        assert result == ['doc2', 'doc1']

    
    def test_get_inverted_index(self):
        doc1 = {'id': 'doc1', 'text': 'some text'}
        doc2 = {'id': 'doc2', 'text': 'some text too'}
        docs = [doc1, doc2]

        index = {
            'some': ['doc1', 'doc2'],
            'text': ['doc1', 'doc2'],
            'too': ['doc2']
        }
        
        assert get_inverted_index(docs) == index
