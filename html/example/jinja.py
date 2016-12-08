#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python script for GWSGI server
import json
import logging
from jinja2 import Environment, PackageLoader

def index(environ, response):
    logger = logging.getLogger()
    logger.debug("jinja.index(%s)", environ)
    status = "200"
    tpl_env = Environment(loader=PackageLoader('example.jinja', 'template'))
    # Reading input data
    data = ""
    if environ["REQUEST_METHOD"] != "GET":
        data_input = environ["wsgi.input"].read().decode("utf-8")
        if data_input:
            try:
                data = json.loads(data_input)
            except:
                data = data_input
                pass
    environ["gwsgi_data"] = data
    if environ["gwsgi_mime"] == "json":
        response_headers = [("Content-type", "application/json")]
        response(status, response_headers)
        return([str(environ).encode("utf-8")])
        #return([json.dumps(output).encode("utf-8")])
    elif environ["gwsgi_mime"] == "html":
        response_headers = [("Content-type", "text/html")]
        response(status, response_headers)
        template = tpl_env.get_template('page.html')
        output = template.render(title="GWSGI:Jinja2 example", environ=environ)
        return([output.encode("utf-8")])
    elif environ["gwsgi_mime"] == "txt":
        response_headers = [("Content-type", "text/plain")]
        response(status, response_headers)
        template = tpl_env.get_template('page.txt')
        output = template.render(title="GWSGI:Jinja2 example", environ=environ)
        return([output.encode("utf-8")])
    else:
        status = "404"
        response_headers = [("Content-type", "text/plain")]
        response(status, response_headers)
        output = "Sorry, the requested MIME_TYPE(%s) is not managed..." % environ["gwsgi_mime"]
        return([output.encode("utf-8")])

# To use directly from bash, try:
# REQUEST_METHOD=GET gwsgi_mime=txt ./env.py
def display(status,header):
    print(status,header)
if __name__ == "__main__":
    import os, sys
    result = index(os.environ, display)
    print(result)
