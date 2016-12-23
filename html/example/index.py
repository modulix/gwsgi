#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python script for GWSGI server
import sys
import os
import logging

def index(environ):
    logger = logging.getLogger()
    logger.debug("index.index(%s)", environ)
    output = """
    <html>
        <header>
            <title>gwsgi:example:index</title>
        </header>
        <body>
            <h1>gwsgi:example:index</h1>
            <h2>Usage examples</h2>
            <h3>env.py</h3>
            <ul>
                <li><a href="/example/env/index.txt?a=aaa&b=bbbb&c=ccccc">env.txt</a></li>
                <li><a href="/example/env/index.html?a=aaa&b=bbbb&c=ccccc">env.html</a></li>
                <li><a href="/example/env/index.json?a=aaa&b=bbbb&c=ccccc">env.json</a></li>
            </ul>
            <h3>jinja.py</h3>
            <ul>
                <li><a href="/example/jinja/index.txt?a=aaa&b=bbbb&c=ccccc">jinja.txt</a></li>
                <li><a href="/example/jinja/index.html?a=aaa&b=bbbb&c=ccccc">jinja.html</a></li>
                <li><a href="/example/jinja/index.json?a=aaa&b=bbbb&c=ccccc">jinja.json</a></li>
            </ul>
            <h3>database.py</h3>
            <ul>
                <li><a href="../database/index.html">database.html</a></li>
            </ul>
        </body>
    </html>
    """
    return([output.encode("utf-8")])

# To be able also to test from bash for debug purpose
# cd $HTML_DIR
# REQUEST_METHOD=GET wsgi_mime=html ./example/index.py
if __name__ == "__main__":
    print(index(os.environ))
