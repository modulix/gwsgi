#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python script for GWSGI server
import json
import logging

def index(environ, response):
    logger = logging.getLogger()
    logger.debug("env.index(%s)", environ)
    status = "200"
    data = ""
    # Reading input data
    if environ["REQUEST_METHOD"] != "GET":
        data_input = environ["wsgi.input"].read().decode("utf-8")
        if data_input:
            try:
                data = json.loads(data_input)
            except:
                pass
    if environ["gwsgi_mime"] == "json":
        response_headers = [("Content-type", "application/json")]
        response(status, response_headers)
        output = {"ENVIRON": environ, "RESPONSE_STATUS": status, "RESPONSE_HEADERS": response_headers, "gwsgi_data": data}
        return([str(output).encode("utf-8")])
        #return([json.dumps(output).encode("utf-8")])
    elif environ["gwsgi_mime"] == "html":
        response_headers = [("Content-type", "text/html")]
        response(status, response_headers)
        output = ""
        tbl = ["RESPONSE_STATUS=%s" % status, "RESPONSE_HEADERS=%s" % str(response_headers), "gwsgi_data=%s" % data]
        for value in environ:
            tbl.append("%s=%s" % (value,environ[value]))
        tbl = sorted(tbl)
        for it in tbl:
            output += "<li>" + it + "</li>"
        output = "<ul>" + output + "</ul>"
        return([output.encode("utf-8")])
    elif environ["gwsgi_mime"] == "txt":
        response_headers = [("Content-type", "text/plain")]
        response(status, response_headers)
        tbl = ["RESPONSE_STATUS=%s" % status, "RESPONSE_HEADERS=%s" % str(response_headers), "gwsgi_data=%s" % data]
        for value in environ:
            tbl.append("%s=%s" % (value,environ[value]))
        tbl = sorted(tbl)
        output = "\n".join(tbl)
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
