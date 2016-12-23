#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python script for GWSGI server
import sys
import os
import json
import logging
from jinja2 import Environment, PackageLoader

def index(environ):
    logger = logging.getLogger()
    logger.debug("jinja.index(%s)", environ)
    tpl_env = Environment(loader=PackageLoader('example.jinja', 'template'))
    if os.path.isfile("example/template/page.%s" % environ["wsgi_mime"]):
        template = tpl_env.get_template('page.%s' % environ["wsgi_mime"])
        output = template.render(title="GWSGI:Jinja2 example", environ=environ)
    else:
        environ["wsgi_status"] = "404"
        environ["wsgi_header"] = [("Content-type", "text/plain")]
        output = "Sorry, the requested MIME type (%s) is not available..." % environ["wsgi_mime"]
    return([output.encode("utf-8")])

# To use directly from bash, you need to cd $HTTP_DIR and try:
# REQUEST_METHOD=GET wsgi_mime=txt ./example/jinja.py
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(index(os.environ))
