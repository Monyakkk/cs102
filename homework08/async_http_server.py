import asyncore
import asynchat
import socket
import multiprocessing
import logging
import mimetypes
import os
from urllib.parse import parse_qs
import urllib
import argparse
from time import strftime, gmtime


def url_normalize(path):
    if path.startswith("."):
        path = "/" + path
    while "../" in path:
        p1 = path.find("/..")
        p2 = path.rfind("/", 0, p1)
        if p2 != -1:
            path = path[:p2] + path[p1+3:]
        else:
            path = path.replace("/..", "", 1)
    path = path.replace("/./", "/")
    path = path.replace("/.", "")
    return path


class FileProducer(object):


    def __init__(self, file, chunk_size=4096):
        self.file = file
        self.chunk_size = chunk_size

    def more(self):
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file.close()
            self.file = None
        return ""

class AsyncServer(asyncore.dispatcher):


    def __init__(self, host="127.0.0.1", port=9000):
        super().__init__()
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        

    def handle_accepted(self):
        log.debug(f"Incoming connection from {addr}")
        AsyncHTTPRequestHandler(sock)

    def serve_forever(self):
        asyncore.loop()
        
        

class AsyncHTTPRequestHandler(asynchat.async_chat):


    def __init__(self, sock):
        super().__init__(sock)
        self.set_terminator(b"\r\n\r\n")
        self.reading_headers = True
        
    def collect_incoming_data(self, data):
        log.debug(f"Incoming data: {data}")
        self._collect_incoming_data(data)

    def found_terminator(self):  
        self.parse_request()

    def parse_request(self):  
        if self.reading_headers:
            self.reading_headers = False
            if not self.parse_headers():
                self.send_error(400)
                self.handle_close()
                return
            
            if self.method == 'POST':
                clne = self.headers.get('Content-Length', 0)
                if int(clen) > 0:
                    self.set_terminator(int(clen))
                else:
                    self.handle_request()
            else:
                self.set_terminator(None)
                self.handle_request()
        else:
            self.set_terminator(None)
            self.request_body = self._get_data()
            self.handle_request()

    def parse_headers(self):    
        key_value_strings = self.ibuffer.split('\r\n')
        for key_value in key_value_strings:
            if ':' not in key_value:
                continue
            else:
                key, value = key_value.split(':', 1)
                value.lstrip()
                self.headers[key.lower()] = value
        self.headers['method'] = self.method

    def handle_request(self):
        method_name = 'do_' + self.method
        if not hasattr(self, method_name):
            self.send_error(405)
            self.handle_close()
            return
        handler = getattr(self, method_name)
        handler()

    def send_header(self, keyword, value):  
        self.response += "{}: {}\r\n".format(keyword, value)

    def send_error(self, code, message=None):
        try:
            short_msg, long_msg = self.responses[code]
        except KeyError:
            short_msg, long_msg = '???', '???'
        if message is None:
            message = short_msg

        self.send_response(code, message)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Connection", "close")
        self.end_headers()

    def send_response(self, code, message=None):    #TODO
        pass

    def end_headers(self):  #TODO
        pass

    def date_time_string(self):  #TODO
        pass

    def send_head(self):  #TODO
        pass

    def translate_path(self, path):  #TODO
        pass

    def do_GET(self):  #TODO
        pass

    def do_HEAD(self):  #TODO
        pass

    responses = {
        200: ('OK', 'Request fulfilled, document follows'),
        400: ('Bad Request',
            'Bad request syntax or unsupported method'),
        403: ('Forbidden',
            'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
            'Specified method is invalid for this resource.'),
    }

def parse_args():
    parser = argparse.ArgumentParser("Simple asynchronous web-server")
    parser.add_argument("--host", dest="host", default="127.0.0.1")
    parser.add_argument("--port", dest="port", type=int, default=9000)
    parser.add_argument("--log", dest="loglevel", default="info")
    parser.add_argument("--logfile", dest="logfile", default=None)
    parser.add_argument("-w", dest="nworkers", type=int, default=1)
    parser.add_argument("-r", dest="document_root", default=".")
    return parser.parse_args()


def run(args):
    server = AsyncServer(host=args.host, port=args.port)
    server.serve_forever()


if __name__ == "__main__":
    args = parse_args()

    logging.basicConfig(
        filename=args.logfile,
        level=getattr(logging, args.loglevel.upper()),
        format="%(name)s: %(process)d %(message)s")
    log = logging.getLogger(__name__)

    DOCUMENT_ROOT = args.document_root
    for _ in range(args.nworkers):
        p = multiprocessing.Process(target=run(args))
        p.start()

        
