#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python script for GWSGI server
import json
import logging

def index(environ, response):
    logger = logging.getLogger()
    logger.debug("index.index(%s)", environ)
    status = "200"
    # This page is available only in HTML format
    response_headers = [("Content-type", "text/html")]
    logger.info("index.index(status=%s,response_headers=%s)", status, response_headers)
    response(status, response_headers)
    output = """
    <html>
        <header>
            <title>gwsgi:index</title>
        </header>
        <body>
            <h1>gwsgi:index</h1>
            <h2>Examples</h2>
            <h3>env.py</h3>
            <ul>
                <li><a href="example/env/index.txt?a=aaa&b=bbbb&c=ccccc">env.txt</a></li>
                <li><a href="example/env/index.html?a=aaa&b=bbbb&c=ccccc">env.html</a></li>
                <li><a href="example/env/index.json?a=aaa&b=bbbb&c=ccccc">env.json</a></li>
            </ul>
            <h3>jinja.py</h3>
            <ul>
                <li><a href="example/jinja/index.txt?a=aaa&b=bbbb&c=ccccc">jinja.txt</a></li>
                <li><a href="example/jinja/index.html?a=aaa&b=bbbb&c=ccccc">jinja.html</a></li>
                <li><a href="example/jinja/index.json?a=aaa&b=bbbb&c=ccccc">jinja.json</a></li>
            </ul>
        </body>
    </html>
    """
    return([output.encode("utf-8")])

# To be able also to test from bash for debug purpose
def display(status,header):
    print(status,header)
if __name__ == "__main__":
    import os
    result = index(os.environ, display)
    print(result)
