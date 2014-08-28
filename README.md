# About

This is simple web server generator. It creates web server using declarative json spec.
It is useful for testing http-based libs and for learning curl commands.

# Use case

Suppose you are writing or testing http library for programming language. This
tool enables you to define web server using json config without boilerplate code.

# Configuration

JSON should include list of accepted endpoints. Each endpoint consists of following
fields:

1. `method`("GET", "POST" etc.., string) - mandatory.
2. `url`(string) - mandatory
3. `request`(object) - mandatory.
4. `on_fail` and `on_success` objects are optional.


`request` object may defines `headers`(array of objects) and `query_params`(object).

`on_fail` and `on_success` should be defined as:

1. `body`(response text, string) - optional
2. `status`(response code, number) - mandatory.
3. `headers`(array) - optional.

If `on_fail` object isn't defined then defult failure response is `{"status": 400, "body": "error occured"}`.
If `on_success` object isn't defined then default succesive response is `{"status": 200, "body": "success"}`.

In case of no one of the provided endpoints are matched then server returns `{"status": 400, "body": "match error"}`.

For config example take a look at `config.json` in root of the repo.

# Installation and using

1. Install requirements from requirements.txt.
2. Run `python run.py -c path_to_config -p port`. By default
`path_to_config=config.json` and `port=8080`

# TODO
3. Logging.
4. More examples.

