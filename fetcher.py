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

from counter_cache import CCache


def get_words(text):
    '''
        Cleare HTML text from tags
        Using example:
            _get_words("<h1>They were not!</h1>") ->
            ["they", "were", "not"]
    '''
    return re.findall(r'[a-zа-я]+', text.lower())


async def fetch(result, session, urls_q, cache):
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
                cache.extend(tokens)
                top_k_words = cache.get_top_k()
                cache.clear()
                result[url] = top_k_words
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

    print('DONE')


async def crawl(result, session, urls_path='urls.txt', batch_size=50, n_threads=5):
    '''
        Create tasks for async reading urls frome file
        and creating n_threads tasks of fetchers
    '''
    urls_q = asyncio.Queue(maxsize=batch_size)

    read_task = asyncio.create_task(read_urls(urls_q, urls_path))
    # Просто передать управление через await asyncio.sleep(0)
    # Оказалось недостаточно, потому что в await urls_q.put()
    # Он его возвращает, доходит до await urls_q.join()
    # Но передача управления не срабатывает, потому что очередь пустая
    # Поэтому гарантировано кладём в очередь элемент при помощи while
    while urls_q.empty():
        print('!')
        await asyncio.sleep(0)

    cache = CCache()
    tasks = [
        asyncio.create_task(fetch(result, session, urls_q, cache))
        for _ in range(n_threads)
    ]

    await urls_q.join()

    print(f'SIZE :: {urls_q.qsize()}')
    read_task.cancel()
    for task in tasks:
        task.cancel()

parser = ArgumentParser()
parser.add_argument('-c', type=int, nargs='?')
parser.add_argument('i', type=int, nargs='?')
parser.add_argument('f', type=str)

async def main(n_threads=10, urls_path='urls.txt'):
    t1 = time.perf_counter()
    async with aiohttp.ClientSession() as session:
        urls_data = {}
        await crawl(
                urls_data,
                session,
                urls_path=urls_path,
                n_threads=n_threads,
                batch_size=75
            )

    print(urls_data, len(urls_data.keys()))
    t2 = time.perf_counter()
    print(f"Time :: {t2 - t1}s")


if __name__ == '__main__':
    args = parser.parse_args()
    n_threads_arg = vars(args)['c'] or vars(args)['i']
    urls_path_arg = vars(args)['f']

    asyncio.run(main(n_threads_arg, urls_path_arg))
