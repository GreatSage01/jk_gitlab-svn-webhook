#!/usr/bin/env python3
# encoding: utf-8
#

from flask import Flask
from apis.my_common_api import *


app = Flask(__name__)
app.config.from_pyfile("settings.py")
app.register_blueprint(my_common_api, url_prefix='/v1')


@app.route('/')
def index():
    return 'hello flask'


def main():
    app.run(host='0.0.0.0', port=8888)


if __name__ == '__main__':
    main()

