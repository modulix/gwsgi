#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python script for GWSGI server
import json
import logging

def index(environ):
    logger = logging.getLogger()
    logger.debug("env.index(%s)", environ)
    if environ["wsgi_mime"] == "json":
        return([str(environ).encode("utf-8")])
        #return([json.dumps(environ).encode("utf-8")])
    elif environ["wsgi_mime"] == "html":
        tbl = []
        for value in environ:
            tbl.append("%s = %s" % (value,environ[value]))
        tbl = sorted(tbl)
        output = ""
        for it in tbl:
            output += "<li>" + it + "</li>"
        output = "<ul>" + output + "</ul>"
        return([output.encode("utf-8")])
    elif environ["wsgi_mime"] == "txt":
        tbl = []
        for value in environ:
            tbl.append("%s=%s" % (value,environ[value]))
        tbl = sorted(tbl)
        output = "\n".join(tbl)
        return([output.encode("utf-8")])
    else:
        environ["wsgi_status"] = "404"
        environ["wsgi_header"] = [("Content-type", "text/plain")]
        output = "Sorry, the requested MIME type(%s) is not available..." % environ["wsgi_mime"]
        return([output.encode("utf-8")])

# To use directly from bash, you need to cd $HTTP_DIR and try:
# REQUEST_METHOD=GET wsgi_mime=txt ./example/env.py
if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(index(os.environ))

