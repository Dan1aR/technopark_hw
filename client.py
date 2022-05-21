'''
    Client command line util
    for load urls from file to
    server and get response in
    many Thread
    Using example:
        python3 client.py 10 urls.txt
'''

from argparse import ArgumentParser
from queue import Queue
import threading
import socket
import json
from urllib import response


def split(arr, n_folds):
    '''
        Splits your arr into N Folds
        Using example:
            split(['1', '2', '3', '4'], 2) ->
            [
                ['1', '2'],
                ['3', '4']
            ]
    '''
    quo, rem = divmod(len(arr), n_folds)
    return (arr[i*quo+min(i, rem):(i+1)*quo+min(i+1, rem)]
            for i in range(n_folds))


def client_worker(response_q, urls: list):
    '''
        Works in his own thread
        send url -> server and waiting for response
        Using example:
            client_worker(['1', '2'])
    '''
    sock = socket.socket()
    sock.connect(('', 8080))

    for url in urls:
        sock.send(url.encode("utf-8"))
        data = json.loads(sock.recv(1024).decode("utf-8"))
        response_q.put(data)
        print(data)

    sock.close()


def main(n_threads, urls_file):
    '''
        main function wich creates n threads
        for each worker and join all of them after
    '''
    with open(urls_file, 'r', encoding="utf-8") as fin:
        urls = [line.strip() for line in fin.readlines()]

    response_q = Queue()

    threads = []
    urls_by_client = split(urls, n_threads)
    for i, c_urls in enumerate(urls_by_client):
        threads.append(
            threading.Thread(
                target=client_worker,
                args=(response_q, c_urls,)
            )
        )
        threads[i].start()

    for worker_th in threads:
        worker_th.join()

    print(f'Received: {response_q.qsize()}')


parser = ArgumentParser()
parser.add_argument('ints', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('strs', metavar='N', type=str, nargs='+',
                    help='an integer for the accumulator')


if __name__ == '__main__':
    args = parser.parse_args()
    n = vars(args)['ints'][0]
    urls_path = vars(args)['strs'][0]
    main(n, urls_path)
