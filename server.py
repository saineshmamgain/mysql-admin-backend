# File: server.py
# Created By: Sainesh Mamgain
# Email: saineshmamgain@gmail.com
# Date: 7/6/18
# Time: 11:00 AM

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse
from importlib import import_module
from modules import Errors


class S(BaseHTTPRequestHandler):

    def _set_headers(self, response_type=200, headers={}):
        self.send_response(response_type)
        if len(headers) > 0:
            for key, header in headers.items():
                self.send_header(keyword=key, value=header)
        self.end_headers()

    def get_module_name(self, module_name):
        return ''.join(word.capitalize() for word in module_name.split('-'))

    def get_module(self):
        parsed = urlparse(self.path)
        print('path:', parsed)
        path = parsed.path
        if path == '/':
            return None
        else:
            path = path.split('/')
            path = list(filter(None, path))
            module = self.get_module_name(path[0])
            if len(path) == 2:
                return {'module': module, 'action': path[1]}
            else:
                return 0

    def handle_request(self):
        module_list = self.get_module()
        if module_list is None:
            self.send_the_response(response_type=200, headers={'Content-Type': 'application/json'}, body=json.dumps({'status': 1, 'message': 'success'}))
        elif module_list == 0:
            response = Errors.error404()
            self.send_the_response(response['type'], response['headers'], response['body'])
        else:
            mod = import_module('modules.' + module_list['module'])
            action = getattr(mod, module_list['action'])
            response = action()
            self.send_the_response(response['type'],response['headers'],response['body'])


    def send_the_response(self, response_type, headers, body):
        self._set_headers(response_type=response_type, headers=headers)
        self.wfile.write(body.encode())

    def do_GET(self):
        self.handle_request()


def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server at http://127.0.0.1:'+ str(port))
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()
