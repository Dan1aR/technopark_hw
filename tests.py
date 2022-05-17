'''
    Async testing for fetch
    Using example:
        python3 tests.py
'''

import asyncio
import os
import unittest

import aiohttp
from aiohttp.test_utils import AioHTTPTestCase

import fetcher
from counter_cache import CCache


class FetcherTest(AioHTTPTestCase):
    '''
        Tests for fether async methods
    '''
    def setUp(self):
        self.urls_test = [
            'https://attackontitan.fandom.com\n',
            'https://attackontitan.fandom.com/wiki/Levi_Ackermann_(Anime)\n',
            'https://attackontitan.fandom.com/wiki/Eren_Jaeger_(Anime)\n',
        ]
        self.urls_file = 'urls_test.txt'
        with open(self.urls_file, 'w', encoding='utf-8') as fout:
            fout.writelines(self.urls_test)

    def tearDown(self):
        os.remove(self.urls_file)

    async def test_crawl(self):
        '''
            Testing crawl function with tests urls
            It could probably Fail, web-siyes might change
            but right now it works :)
        '''
        result = {}
        await fetcher.crawl(
            result,
            urls_path=self.urls_file,
            batch_size=5,
            n_threads=5
        )

        expected = {
                "http://example.com": {
                    "width": 5, "domain": 4, "example": 3,
                    "content": 3, "text": 3, "color": 3,
                    "margin": 3, "auto": 3, "in": 3,
                    "charset": 2
                },
                "https://attackontitan.fandom.com": {
                    'wiki': 1054, 'wds': 905, 'data': 897,
                    'fandom': 711, 'com': 640, 'level': 524,
                    'anime': 509, 'tracking': 506, 'image': 440,
                    'http': 434
                },
                "https://attackontitan.fandom.com/wiki/Levi_Ackermann_(Anime)": {
                    'levi': 1105, 'the': 1094,
                    'data': 1060, 'anime': 1037,
                    'wiki': 1009, 'wds': 889, 'to': 827,
                    'png': 590, 'titan': 583, 'fandom': 550
                },
                "https://attackontitan.fandom.com/wiki/Eren_Jaeger_(Anime)": {
                    'the': 1850, 'anime': 1599, 'eren': 1573,
                    'to': 1414, 'data': 1366, 'wiki': 1247,
                    'titan': 1219, 'wds': 849, 'and': 786,
                    'image': 755
                }
            }

        self.assertDictEqual(result, expected)

    async def test_fetch(self):
        '''
            Testing Fetch function - you could experience
            same issues as with crawl test

            Fetch is a small part of crawl
        '''
        result = {}

        test_q = asyncio.Queue()
        await test_q.put(self.urls_test[0].strip())

        async with aiohttp.ClientSession() as session:
            task = asyncio.create_task(fetcher.fetch(
                result,
                session,
                test_q
            ))

            await test_q.join()

        expected = {
                "https://attackontitan.fandom.com": {
                    'wiki': 1054, 'wds': 905, 'data': 897,
                    'fandom': 711, 'com': 640, 'level': 524,
                    'anime': 509, 'tracking': 506, 'image': 440,
                    'http': 434
                }
            }

        print(result)
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
