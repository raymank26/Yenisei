from yenisei import utils, server, cli

from http.server import HTTPServer
from colorama import init
from jsonschema import validate

import json


if __name__ == "__main__":
    args = cli.parser.parse_args()
    config_file = open(args.config_path)
    config = json.loads(config_file.read())
    validate(config, utils.SCHEMA)
    server.Handler.config = config

    # switch to ascii
    init()

    # start server
    server = HTTPServer(('localhost', args.port), server.Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()

