'''
    URL async fetcher
    Using example:
        python3 fetcher.py -с 10 urls.txt
'''

from argparse import ArgumentParser
import re
import time
import asyncio
import aiohttp
import aiofiles

from counter_cache import CCash


def get_words(text):
    '''
        Cleare HTML text from tags
        Using example:
            _get_words("<h1>They were not!</h1>") ->
            ["they", "were", "not"]
    '''
    return re.findall(r'[a-zа-я]+', text.lower())


async def fetch(session, urls_q):
    '''
        Fetcher - tries to get url from queue
        and work with it using CCash to get
        top k words
    '''
    while True:
        url = await urls_q.get()
        try:
            async with session.get(url) as resp:
                data = await resp.read()
                tokens = get_words(data.decode('utf-8'))
                cache = CCash(tokens)
                print(cache.get_top_k())
        finally:
            urls_q.task_done()


async def read_urls(urls_q, urls_path='urls.txt'):
    '''
        Function for async reading urls from file
        and put url into queue
    '''
    async with aiofiles.open(urls_path, 'r') as fin:
        async for line in fin:
            await urls_q.put(line.strip())


async def crawl(urls_path='urls.txt', n_threads=5):
    '''
        Create tasks for async reading urls frome file
        and creating n_threads tasks of fetchers
    '''
    urls_q = asyncio.Queue()
    # Заглушка, чтобы q.join() начал работать
    await urls_q.put('http://example.com')

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(read_urls(urls_q, urls_path))]

        for _ in range(n_threads):
            tasks.append(asyncio.create_task(fetch(session, urls_q)))

        await urls_q.join()

    for task in tasks:
        task.cancel()

parser = ArgumentParser()
parser.add_argument('-c', type=int, nargs='?')
parser.add_argument('i', type=int, nargs='?')
parser.add_argument('f', type=str)

if __name__ == '__main__':
    args = parser.parse_args()
    n_threads_arg = vars(args)['c'] or vars(args)['i']
    urls_path_arg = vars(args)['f']

    t1 = time.perf_counter()
    asyncio.run(crawl(urls_path_arg, n_threads_arg))
    t2 = time.perf_counter()
    print(f"Time :: {t2 - t1}s")
