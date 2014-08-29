from .utils import log_request_object, to_list, process_body


from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
# import urlparse

# from BaseHTTPServer import HTTPServer


class Request:
    def __init__(self, headers, query_params, body=None):
        self.headers = headers
        self.body = body
        self.query_params = query_params

    def __eq__(self, other):
        for header in self.headers:
            flag = False
            for other_header in other.headers:
                if header == other_header:
                    flag = True
            if not flag:
                return False
        return self.query_params == other.query_params and\
            self.body == other.body

    def __str__(self):
        s = "headers: {}\nbody: {}\nquery_params: {}\n".format(
            self.headers, self.body, self.query_params
        )
        return s



class Response:
    def __init__(self, body, headers, status):
        self.body = body
        self.headers = to_list(headers)
        self.status = status


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.validate()

    def do_POST(self):
        self.validate()

    def do_HEAD(self):
        self.validate()

    def do_PUT(self):
        self.validate()

    def do_OPTIONS(self):
        self.validate()

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
        body = response.body
        self.wfile.write(bytes(body, encoding))

    def validate(self):
        matched_item = None
        query_params = {}
        parsed_path = urlparse(self.path)
        if parsed_path.query:
            for item in parsed_path.query.split('&'):
                key, value = item.split('=')
                query_params[key] = value


        for item in self.config:
            if item['method'] == self.command and item['url'] == parsed_path.path:
                matched_item = item
                break

        if not matched_item:
            self.return_response(Response(status=400,
                body="match error",
                headers={}))
            return

        request_from_config = Request(
            headers=to_list(matched_item['request'].get('headers', [])),
            query_params=matched_item['request'].get('query_params', {}),
            body=matched_item['request'].get("data")
            )
        request_from_server = Request(
            headers=self.headers.items(),
            query_params=query_params,
            body=process_body(self),
            )
        if request_from_config != request_from_server:
            print(request_from_config)
            print(request_from_server)
            on_fail = matched_item.get('on_fail', {
                "status": 400,
                "body": "error occured",
                "headers": [],
                })
            self.return_response(Response(**on_fail))
        else:
            on_success = matched_item.get('on_success', {
                "status": 200,
                "body": "success",
                "headers": [],
                })
            self.return_response(Response(**on_success))
