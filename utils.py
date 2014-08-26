from colorama import Fore, Back, Style

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
