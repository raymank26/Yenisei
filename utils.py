from colorama import Fore, Back, Style
import cgi
import os

# __all__ = ['log_success', 'log_error', 'log_request_object']

def log_success(handler):
    log_request(Fore.GREEN, handler)

def log_request(color, handler):
    print("{}Method: {}, path: {}".format(
        color, handler.command, handler.path))
    print(Fore.RESET)

def log_error(handler):
    log_request(Fore.RED, handler)


def log_request_object(request):
    print(
        "headers: {}, query_params: {}".format(
            request.headers, request.query_params)
        )

def to_list(headers):
    "transforms list of dicts to list of tuples"
    result = []
    # import pdb
    # pdb.set_trace()
    if headers:
        for header in headers:
            for key, value in header.items():
                result.append((key, value))
    return result


def process_body(handler):
    form = cgi.FieldStorage(
        fp=handler.rfile,
        headers=handler.headers,
        environ={
            "REQUEST_METHOD": handler.command,
            "CONTENT_TYPE": handler.headers['Content-Type']
        }
        )
    files = []
    form_items = []
    for field in form.keys():
        field_item = form[field]
        if field_item.filename:
            file_object = field_item.file
            file_object.seek(0, os.SEEK_END)
            files.append({
                "length": file_object.tell(),
                "name": field_item.filename
                })
        else:
            form_items.append({
                field: form[field].value
                })
    return {
        "files": files,
        "form": form_items
    }
