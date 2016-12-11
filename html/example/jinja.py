#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python script for GWSGI server
import json
import logging
from jinja2 import Environment, PackageLoader

def index(environ):
    logger = logging.getLogger()
    logger.debug("jinja.index(%s)", environ)
    tpl_env = Environment(loader=PackageLoader('example.jinja', 'template'))
    if environ["wsgi_mime"] == "json":
        return([str(environ).encode("utf-8")])
        #return([json.dumps(output).encode("utf-8")])
    elif environ["wsgi_mime"] == "html":
        template = tpl_env.get_template('page.html')
        output = template.render(title="GWSGI:Jinja2 example", environ=environ)
        return([output.encode("utf-8")])
    elif environ["wsgi_mime"] == "txt":
        template = tpl_env.get_template('page.txt')
        output = template.render(title="GWSGI:Jinja2 example", environ=environ)
        return([output.encode("utf-8")])
    else:
        environ["wsgi_status"] = "404"
        environ["wsgi_header"] = [("Content-type", "text/plain")]
        output = "Sorry, the requested MIME_TYPE(%s) is not managed..." % environ["wsgi_mime"]
        return([output.encode("utf-8")])

# To use directly from bash, try:
# REQUEST_METHOD=GET wsgi_mime=txt ./html/jinja.py
if __name__ == "__main__":
    import os
    print(index(os.environ))
