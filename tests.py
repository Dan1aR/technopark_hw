from linecache import cache
import unittest
from counter_cache import CCash
import client
from server import Server

class TestCCache(unittest.TestCase):
    def test_add(self):
        cache = CCash()
        self.assertEqual(cache.data, {})
        cache.add('word')
        cache.add('word')
        cache.add('word1')
        self.assertEqual(cache.data, {'word':2, 'word1':1})

    def test_init_from_list(self):
        elems = [
            [f'word{j}' for i in range(j)]
            for j in range(1, 6)
        ]
        elems = [item for sublist in elems for item in sublist]
        cache = CCash(elems)
        self.assertEqual(cache.data, {
            f'word{i}':i for i in range(1, 6)
        })

    def test_get_top_k(self):
        elems = [
            [f'word{j}' for i in range(j)]
            for j in range(1, 6)
        ]
        elems = [item for sublist in elems for item in sublist]
        cache = CCash(elems, top_k=3)
        self.assertEqual(cache.get_top_k(), {
            f'word{i}':i for i in range(3, 6)
        })


class TestClient(unittest.TestCase):
    def test_split(self):
        urls = [f'url_{i}' for i in range(10)]
        urls_s = [u for u in client.split(urls, 2)]
        self.assertEqual(urls_s,[
            [f'url_{i}' for i in range(0+5*n, 5+5*n)] for n in range(2)
        ])


class TestServer(unittest.TestCase):
    def test_get_words(self):
        HTML = """
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
        server = Server()
        words = server._get_words(HTML)
        self.assertEqual(words_t, words)


if __name__ == '__main__':
    unittest.main()