'''
    Server implementation
    To calculate most popular words on web-site
'''

from argparse import ArgumentParser
from urllib.error import HTTPError
from urllib.request import urlopen
from queue import Queue
import threading
import socket
import json
import time
import re
from counter_cache import CCash

def _get_words(text):
    '''
        Cleare HTML text from tags
        Using example:
            _get_words("<h1>They were not!</h1>") ->
            ["they", "were", "not"]
    '''
    return re.findall(r'[a-zа-я]+', text.lower())


class Server():
    '''
        Server using example:
            server = Server(num_workers=10, num_words=5)
            server.loop()
    '''
    def __init__(self, num_workers=10, num_words=5):
        self.num_workers = num_workers
        self.num_words = num_words
        self.workers = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clients = set()
        self.clients_to_remove = set()
        self.tasks_queue = Queue()  # Don't need to use Lock for it

        self.tick_rate = 1
        self.sock.settimeout(self.tick_rate)

        # For statistics
        self.total_urls = 0
        self.th_lock = threading.Lock()

    def _print_clients(self):
        print('Clients in set:', len(self.clients))

    def _print_statistic(self):
        self.th_lock.acquire() # pylint:disable=R1732
        self.total_urls += 1
        print(f'Total amount of urls = {self.total_urls} ')
        self.th_lock.release()

    def _accept_connection(self):
        try:
            client, addr = self.sock.accept()
        except socket.timeout:
            return
        else:
            # Need this fot Client worker see whole clients
            print('New connection:', addr)
            self.clients.add(client)

    def _recv_from_client(self, client):
        try:
            data = client.recv(4096)
        except socket.timeout:
            return
        else:
            if data != b'':
                print('data from client:', data)
                self.tasks_queue.put((data, client))
            else:
                self.clients_to_remove.add(client)

    def top_k_worker(self, k):
        '''
            Each worker tries to catch (url, client) from tasks_queue
            and work with it;
            Using CCahe to calculate k top words
            Every worker send result to client by himself
            After every url every worker calls _print_statisti
        '''
        while True:
            if not self.tasks_queue.empty():
                url, client = self.tasks_queue.get()
                try:
                    url_file = urlopen(url.decode("utf-8")) # pylint:disable=R1732
                except HTTPError:
                    client.send(b'{}')
                else:
                    text = url_file.read().decode("utf-8")
                    text = _get_words(text)

                    cache = CCash(text, k)
                    client.send(json.dumps(
                            cache.get_top_k()
                        ).encode("utf-8")
                    )

                    self._print_statistic()

            time.sleep(self.tick_rate)

    def loop(self):
        '''
            Master thread here
            in infinite loop it:
                1) tries to accept connection
                    (stop if waiting too long)
                2) tries to get data from every client
                    (stop listening to client if waiting too long)
                3) removes disconnected clients from set

            Too-long-waiting time controlls by tick_rate attr

            Before starting Master create N workers threads
            Each of them tries to catch (url, client) from tasks_queue
            and work with it; Every worker send result to client by himself
            After every url every worker calls _print_statisti
        '''
        self.sock.bind(('', 8080))
        self.sock.listen(100)

        for i in range(self.num_workers):
            self.workers.append(
                threading.Thread(
                    target=self.top_k_worker,
                    args=(self.num_words,)
                )
            )
            self.workers[i].start()

        stop = False
        while not stop:
            # Accept new connection
            self._accept_connection()

            self._print_clients()

            # Get data from current clients
            for i, client in enumerate(self.clients):
                self._recv_from_client(client)

            # Remove disconnected clients from set
            for client_to_remove in self.clients_to_remove:
                self.clients.remove(client_to_remove)

            self.clients_to_remove.clear()

        for worker in self.num_workers:
            worker.join()


parser = ArgumentParser()
parser.add_argument("-w", "--workers", dest="num_workers", type=int,
                    required=True,
                    help="Number of workers to run by server",
                    metavar="num_workers")

parser.add_argument("-k", "--top_k", dest="num_words", type=int,
                    required=True,
                    help="Top K words to calculate",
                    metavar="num_words")


if __name__ == "__main__":
    args = parser.parse_args()
    server = Server(**vars(args))
    server.loop()
