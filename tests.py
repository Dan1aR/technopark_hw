'''
    Async testing for fetch
    Using example:
        python3 tests.py
'''

import asyncio
import os
import unittest
from unittest.mock import MagicMock

import aiohttp
from aiohttp.test_utils import AioHTTPTestCase

import fetcher
from counter_cache import CCache


class MockSessionResp:
    '''
        Awaitable mock object
    '''
    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await asyncio.sleep(0)

    async def read(self): #pylint: disable=R0201
        '''
            Mock for resp.read()
        '''
        html_test = b"""
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
        return html_test


class FetcherTest(AioHTTPTestCase):
    '''
        Tests for fether async methods
    '''
    def setUp(self):
        self.urls_test = [
            'https://attackontitan.fandom.com\n',
            'https://attackontitan.fandom.com/wiki/Levi_Ackermann_(Anime)\n',
            'https://attackontitan.fandom.com/wiki/Eren_Jaeger_(Anime)\n'
        ]
        self.urls_file = 'urls_test.txt'
        with open(self.urls_file, 'w', encoding='utf-8') as fout:
            fout.writelines(self.urls_test)

    def tearDown(self):
        os.remove(self.urls_file)

    async def test_fetch(self):
        '''
            Testing Fetch function - you could experience
            same issues as with crawl test

            Fetch is a small part of crawl
        '''

        test_q = asyncio.Queue()
        await test_q.put("https://attackontitan.fandom.com")

        async with aiohttp.ClientSession() as session:
            session.get = MagicMock(return_value=MockSessionResp())

            result = {}
            counter_cache = CCache()
            task = asyncio.create_task(fetcher.fetch(
                result,
                session,
                test_q,
                counter_cache
            ))

            await test_q.join()

        expected = {
                "https://attackontitan.fandom.com": {
                    'the': 5, 'to': 4, 'my': 4, 'soldiers': 4,
                    'we': 3, 'not': 2, 'their': 2,
                    'as': 2, 'us': 2, 'fallen': 2
                }
            }

        self.assertDictEqual(result, expected)

    async def test_read_urls(self):
        '''
            Test reading urls function
            File generated in setUp method
            and deleted by teardown method
        '''
        test_q = asyncio.Queue()

        await fetcher.read_urls(test_q, self.urls_file)

        urls_result = []
        while not test_q.empty():
            urls_result.append(await test_q.get())

        self.assertEqual(len(urls_result), len(self.urls_test))
        self.assertEqual(
            urls_result,
            list(map(lambda url: url.strip(), self.urls_test))
        )


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


class TestFetcherUtils(unittest.TestCase):
    '''
        Testing utils functions, which are used in fetch
    '''
    def test_get_words(self):
        '''
            test get_words function for
            converting text to clean list of tokens
        '''
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
        words_t = [
            'h', 'they', 'were', 'not', 'h',
            'p', 'h', 'their', 'memory', 'serves',
            'as', 'an', 'example', 'to', 'us',
            'all', 'h', 'the', 'courageous', 'fallen',
            'the', 'anguished', 'fallen', 'p', 'p',
            'their', 'lives', 'have', 'meaning',
            'because', 'p', 'p', 'we', 'the',
            'living', 'refuse', 'to', 'forget',
            'them', 'p', 'div', 'class', 'a', 'and',
            'as', 'we', 'ride', 'to', 'certain',
            'death', 'a', 'a', 'we', 'trust',
            'our', 'successors', 'to', 'do', 'the',
            'same', 'for', 'us', 'a', 'a', 'because',
            'my', 'soldiers', 'do', 'not', 'buckle',
            'or', 'yield', 'a', 'a', 'when', 'faced',
            'with', 'the', 'cruelty', 'of', 'this',
            'world', 'a', 'class', 'div', 'h', 'my',
            'soldiers', 'push', 'forward', 'h', 'h',
            'my', 'soldiers', 'scream', 'out', 'h',
            'h', 'my', 'soldiers', 'raaaaage', 'h'
        ]
        words = fetcher.get_words(html_test)
        self.assertEqual(words_t, words)


if __name__ == '__main__':
    unittest.main()
