import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from colorama import init
from utils import log_request_object
from urllib.parse import urlparse
# import urlparse

# from BaseHTTPServer import HTTPServer

def to_list(headers):
    result = []
    for header in headers:
        for key, value in header.items():
            result.append((key, value))
    return result

class Request:
    def __init__(self, headers, query_params, is_headers_processed=False):
        if is_headers_processed:
            self.headers = headers
        else:
            self.headers = to_list(headers)

        self.query_params = query_params
    def __eq__(self, other):
        for header in self.headers:
            flag = False
            for other_header in other.headers:
                if header == other_header:
                    flag = True
            if not flag:
                return False
        return self.query_params == other.query_params


class Response:
    def __init__(self, body, headers, status):
        self.body = body
        self.headers = to_list(headers)
        self.status = status


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        validate(self)

    def do_POST(self):
        validate(self)

    def do_HEAD(self):
        validate(self)

    def do_PUT(self):
        validate(self)

    def do_OPTIONS(self):
        validate(self)

    def return_response(self, response):
        self.send_response(response.status)
        encoding_defined = False
        encoding = 'UTF-8'

        for header in response.headers:
            key = header[0]
            value = header[1]
            self.send_header(key, value)
            if key == "Content-Type" and "charset=" in value:
                encoding_defined = True
                encoding = value.split('=')[1]
        if not encoding_defined:
            self.send_header("Content-Type", "charset={}".format(encoding))

        self.end_headers()
        body = response.body + "\n"
        self.wfile.write(bytes(body, encoding))

def validate(handler):
    matched_item = None
    query_params = {}
    parsed_path = urlparse(handler.path)
    for item in parsed_path.query.split('&'):
        key, value = item.split('=')
        query_params[key] = value


    for item in handler.config:
        if item['method'] == handler.command and item['url'] == parsed_path.path:
            matched_item = item
            break

    if not matched_item:
        handler.return_response(Response(status=400,
            body="matched error",
            headers={}))
        return

    request_from_config = Request(
        headers=(matched_item['request'].get('headers')),
        query_params=matched_item['request'].get('query_params')
        )
    request_from_server = Request(
        headers=handler.headers.items(),
        query_params=query_params,
        is_headers_processed=True
        )
    if request_from_config != request_from_server:
        log_request_object(request_from_config)
        log_request_object(request_from_server)
        on_fail = matched_item.get('on_fail', {
            "status": 400,
            "body": "error occured",
            "headers": [],
            })
        handler.return_response(Response(**on_fail))
    else:
        on_success = matched_item.get('on_success', {
            "status": 200,
            "body": "success",
            "headers": [],
            })
        handler.return_response(Response(**on_success))


if __name__ == "__main__":
    # load config
    config_file = open("config.json")
    config = json.loads(config_file.read())
    Handler.config = config

    # switch to ascii
    init()

    # start server
    server = HTTPServer(('localhost', 8080), Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

