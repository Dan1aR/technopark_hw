'''
    Tests for client, server and counter_cache
    Using:
        python3 tests.py
'''
import json
import socket
import unittest
from unittest.mock import MagicMock, patch
from queue import Queue

from matplotlib.pyplot import close, connect

import client
import server
from counter_cache import CCache


class TestCCache(unittest.TestCase):
    '''
        Tests for CCache here
        It stores keys and returns most popular once
    '''
    def test_add(self):
        '''
            test add method
        '''
        cache = CCache()
        self.assertEqual(cache.data, {})
        cache.add('word')
        cache.add('word')
        cache.add('word1')
        self.assertEqual(cache.data, {'word': 2, 'word1': 1})

    def test_init_from_list(self):
        '''
            test initialization from list
        '''
        elems = [
            [f'word{j}' for i in range(j)]
            for j in range(1, 6)
        ]
        elems = [item for sublist in elems for item in sublist]
        cache = CCache(elems)
        self.assertEqual(cache.data, {
            f'word{i}': i for i in range(1, 6)
        })

    def test_extend(self):
        '''
            test extending tokens
        '''
        elems = [
            [f'word{j}' for i in range(j)]
            for j in range(1, 6)
        ]
        elems = [item for sublist in elems for item in sublist]
        cache = CCache()
        cache.extend(elems)
        self.assertEqual(cache.data, {
            f'word{i}': i for i in range(1, 6)
        })

    def test_clear(self):
        '''
            test clearing
        '''
        elems = [
            [f'word{j}' for i in range(j)]
            for j in range(1, 6)
        ]
        elems = [item for sublist in elems for item in sublist]
        cache = CCache()
        cache.extend(elems)
        self.assertEqual(cache.data, {
            f'word{i}': i for i in range(1, 6)
        })
        cache.clear()
        self.assertEqual(cache.data, {})

    def test_get_top_k(self):
        '''
            test getting k most popular keys
        '''
        elems = [
            [f'word{j}' for i in range(j)]
            for j in range(1, 6)
        ]
        elems = [item for sublist in elems for item in sublist]
        cache = CCache(elems, top_k=3)
        self.assertEqual(cache.get_top_k(), {
            f'word{i}': i for i in range(3, 6)
        })


class TestClient(unittest.TestCase):
    def setUp(self):
        self.html_test = b"""
            <h1>They were not!</h1>
            <p> <h2> Their memory serves as an example to us all! </h2>
            The courageous fallen! The anguished fallen! </p>
            <p> Their lives have meaning because </p>
            <p> we the living refuse to forget them! </p>
            <div>
            <class> <a> And as we ride to certain death, </a>
            <a> we trust our successors to do the same for us! </a>
            <a> Because my soldiers do not buckle or yield </a>
            <a> when faced with the cruelty of this world! </a> </class>
            </div>
            <h3> My soldiers push forward! </h3>
            <h2> My soldiers scream out! </h2>
            <h1> My soldiers RAAAAAGE! </h1>
        """

        self.top_k_test = {
            'skeleton': 332,
            'box': 276,
            'size': 121,
            'tp': 112
        }

        self.response_test = json.dumps(self.top_k_test).encode("utf-8")

    def test_split(self):
        urls = [f'url_{i}' for i in range(10)]
        urls_s = [u for u in client.split(urls, 2)]
        self.assertEqual(urls_s,[
            [f'url_{i}' for i in range(0+5*n, 5+5*n)] for n in range(2)
        ])

    def test_client_worker(self):
        with patch.multiple(socket.socket,
                    connect=MagicMock(return_value=None),
                    send=MagicMock(return_value=None),
                    recv=MagicMock(return_value=self.response_test),
                ) as mock_socket:
            test_q = Queue()
            test_urls = ['test_url', 'test_url', 'test_url']
            client.client_worker(test_q, test_urls)
        
        while not test_q.empty():
            resp = test_q.get()
            self.assertEqual(resp, self.top_k_test)

class TestServer(unittest.TestCase):
    def test_get_words(self):
        html_test = """
            <h1>They were not!</h1>
            <p> <h2> Their memory serves as an example to us all! </h2>
            The courageous fallen! The anguished fallen! </p>
            <p> Their lives have meaning because </p>
            <p> we the living refuse to forget them! </p>
            <div>
            <class> <a> And as we ride to certain death, </a>
            <a> we trust our successors to do the same for us! </a>
            <a> Because my soldiers do not buckle or yield </a>
            <a> when faced with the cruelty of this world! </a> </class>
            </div>
            <h3> My soldiers push forward! </h3>
            <h2> My soldiers scream out! </h2>
            <h1> My soldiers RAAAAAGE! </h1>
        """
        words_t = ['h', 'they', 'were', 'not', 'h', 'p', 'h', 'their', 'memory', 'serves', 'as', 'an', 'example', 'to', 'us', 'all', 'h', 'the', 'courageous', 'fallen', 'the', 'anguished', 'fallen', 'p', 'p', 'their', 'lives', 'have', 'meaning', 'because', 'p', 'p', 'we', 'the', 'living', 'refuse', 'to', 'forget', 'them', 'p', 'div', 'class', 'a', 'and', 'as', 'we', 'ride', 'to', 'certain', 'death', 'a', 'a', 'we', 'trust', 'our', 'successors', 'to', 'do', 'the', 'same', 'for', 'us', 'a', 'a', 'because', 'my', 'soldiers', 'do', 'not', 'buckle', 'or', 'yield', 'a', 'a', 'when', 'faced', 'with', 'the', 'cruelty', 'of', 'this', 'world', 'a', 'class', 'div', 'h', 'my', 'soldiers', 'push', 'forward', 'h', 'h', 'my', 'soldiers', 'scream', 'out', 'h', 'h', 'my', 'soldiers', 'raaaaage', 'h']
        words = server._get_words(html_test)
        self.assertEqual(words_t, words)


if __name__ == '__main__':
    unittest.main()
