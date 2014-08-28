import argparse

parser = argparse.ArgumentParser(description="declarative web server")

parser.add_argument("--port", type=int, help="server port number", default=8080)
parser.add_argument("--config-path", type=str, help="path to json config file",
    default="config.json")
