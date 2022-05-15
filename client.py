from argparse import ArgumentParser
import threading
import socket
import json


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def client_worker(urls: list):
    sock = socket.socket()
    sock.connect(('', 8080)) 

    for url in urls:
        sock.send(url.encode("utf-8"))
        print( json.loads(sock.recv(1024).decode("utf-8")))

    sock.close()

def main(n, urls_file):
    with open(urls_file, 'r') as fin:
        urls = [line.strip() for line in fin.readlines()]

    threads = []
    urls_by_client = split(urls, n)
    for i, c_urls in enumerate(urls_by_client):
        threads.append(
            threading.Thread(
                target=client_worker,
                args=(c_urls,)
            )
        )
        threads[i].start()

    for th in threads:
        th.join()


parser = ArgumentParser()
parser.add_argument('ints', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('strs', metavar='N', type=str, nargs='+',
                    help='an integer for the accumulator')


if __name__ == '__main__':
    args = parser.parse_args()
    n = vars(args)['ints'][0]
    urls_file = vars(args)['strs'][0]
    main(n, urls_file)
