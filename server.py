import http.server
import json
import urllib.parse
from importlib import import_module
from modules import Errors


class S(http.server.BaseHTTPRequestHandler):

    def _set_headers(self, response_type=200, headers={}):
        self.send_response(response_type)
        if len(headers) > 0:
            for key, header in headers.items():
                self.send_header(keyword=key, value=header)
        self.end_headers()

    def get_module_name(self, module_name):
        return ''.join(word.capitalize() for word in module_name.split('-'))

    def get_module(self):
        parsed = urllib.parse.urlparse(self.path)
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
            self._set_headers(response_type=200, headers={'Content-Type': 'application/json'})
            self.wfile.write(json.dumps({'status': 1, 'message': 'success'}).encode())
        elif module_list == 0:
            response = Errors.error404()
            self._set_headers(response_type=response['type'], headers=response['headers'])
            self.wfile.write(response['body'].encode())
        else:
            mod = import_module('modules.' + module_list['module'])
            action = getattr(mod, module_list['action'])
            response = action()
            self._set_headers(response_type=response['type'], headers=response['headers'])
            self.wfile.write(response['body'].encode())

    def do_GET(self):
        self.handle_request()


def run(server_class=http.server.HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

if len(argv) == 2:
    run(port=int(argv[1]))
else:
    run()
