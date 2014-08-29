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
    if handler.command not in ["POST", "PUT"]:
        return None
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

class RequiredField(Exception):
    pass


SCHEMA = {
    "type": "array",
    "definitions": {
        "headers": {
            "type": "array",
            "items": {
                "type": "object"
            }
        },
        "returned_response": {
            "type": "object",
            "properties": {
                "headers": {
                    "$ref": "#/definitions/headers"
                },
                "body": {
                    "type": "string"
                },
                "status": {
                    "type": "number",
                }
            }
        },
        "base_request": {
            "type": "object",
            "properties": {
                "headers": {
                    "$ref": "#/definitions/headers"
                },
                "query_params": {
                    "type": "object"
                }

            }

        },
        "base_method": {
            "type": "object",
            "required": ["url", "request", "method"],
            "properties": {
                "url": {
                    "type": "string"
                },
                "method": {
                    "type": "string"
                },
                "requrest": {
                    "$ref": "#/definitions/base_request"
                },
                "on_fail": {
                    "$ref": "#/definitions/returned_response"
                },
                "on_success": {
                    "$ref": "#/definitions/returned_response"
                }
            }
        }
    },
    "items": {
        "allOf": [
            {
                "$ref": "#/definitions/base_method",
            },
            {
                "anyOf": [
                    { # explicit request method
                        "type": "object",
                        "properties": {
                            "method": {
                                "type": "string",
                                "pattern": "POST|PUT"
                            },
                            "request": {
                                "type": "object",
                                "properties": {
                                    "data": {
                                        "type": "object",
                                        "properties": {
                                            "files": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "length": {
                                                            "type": "number",
                                                        },
                                                        "name": {
                                                            "type": "string"
                                                        }
                                                    }
                                                }
                                            },
                                            "form": {
                                                "type": "object"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    {
                        "type": "object",
                        "properties": {
                            "method": {
                                "type": "string",
                                "pattern": "GET|HEAD|OPTIONS"
                            }
                        }
                    }
                ]
            }
        ]
    }
}

