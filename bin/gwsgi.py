#!/bin/env python
# -*- coding: utf-8 -*-
# GWSGI : WSGI gevent server
#
import os
import sys
import signal
import gevent
from gevent.pywsgi import WSGIServer
from gevent.pywsgi import WSGIHandler
from gevent.pool import Pool
from datetime import datetime
import importlib
import logging
import argparse
try:
    # Python 3
    from urllib.parse import parse_qs
except ImportError:
    # Python 2
    from urlparse import parse_qs

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from UnixDaemon import UnixDaemon

class GWSGIServer(UnixDaemon):
    def __init__(self, conf):
        super(GWSGIServer, self).__init__(conf.PID_FILE, conf.LOG_FILE)
        if conf.DEBUG:
            logging.basicConfig(filename = conf.LOG_FILE, level = logging.DEBUG, format = conf.LOG_FORMAT, datefmt = "%Y-%m-%d %H:%M:%S")
        else:
            logging.basicConfig(filename = conf.LOG_FILE, level = logging.INFO, format = conf.LOG_FORMAT, datefmt = "%Y-%m-%d %H:%M:%S")
        self.logger = logging.getLogger()
        self.conf = conf
        gevent.signal(signal.SIGQUIT, gevent.kill)
        # Persistant variables
        self.globales = {"gwsgi_count": 0}
    def run(self):
        pool = Pool(self.conf.MAX_CLIENTS)
        self.logger.info("gwsgi server is running at http://%s:%s/" % (self.conf.SERVER, self.conf.PORT))
        wsgi = WSGIServer((self.conf.SERVER, self.conf.PORT), self.handle_wsgi, spawn=pool, handler_class=WSGIHandler)
        wsgi.serve_forever()
    def handle_wsgi(self, environ, response):
        assert environ
        sem = gevent.lock.Semaphore()
        self.globales["gwsgi_count"] += 1
        if environ["PATH_INFO"][-1] == "/":
            path_info = os.path.join(environ["PATH_INFO"][1:], self.conf.DEFAULT_INDEX)
        else:
            path_info = environ["PATH_INFO"][1:]
        (filename, fileextension) = os.path.splitext(path_info)
        if "." in fileextension and fileextension != ".py":
            mime_type = fileextension[1:]
        else:
            mime_type = os.path.splitext(self.conf.DEFAULT_INDEX)[1][1:]
        # Path2Methode : aaa/bbb/ccc.xxx -> aaa.bbb:ccc(mime_type=xxx)
        module = filename.replace("/",".")
        if "." in module:
            (module, methode) = module.rsplit(".", 1)
            filename = os.path.join(self.conf.HTML_DIR, os.path.dirname(filename) + ".py")
        else:
            methode = self.conf.DEFAULT_METHOD
            filename = os.path.join(self.conf.HTML_DIR, filename + ".py")
        self.logger.debug("gwsgi:%s:%s:%s=%s:%s(%s)", environ["PATH_INFO"], path_info, filename, module, methode, mime_type)
        if "gwsgi_" + environ["REQUEST_METHOD"] in self.globales:
            self.globales["gwsgi_" + environ["REQUEST_METHOD"]] += 1
        else:
            self.globales["gwsgi_" + environ["REQUEST_METHOD"]] = 1
        if "HTTP_X_REAL_IP" in environ:
            self.globales["gwsgi_ip"] = environ["HTTP_X_REAL_IP"]
        else:
            self.globales["gwsgi_ip"] = environ["REMOTE_ADDR"]
        if os.path.isfile(filename) and methode[0:1] != "_":
            module = importlib.import_module(module)
            args = {}
            args = parse_qs(environ["QUERY_STRING"])
            self.globales["gwsgi_query"] = args
            self.globales["gwsgi_mime"] = mime_type
            try:
                env = dict(environ)
                env.update(self.globales)
                output = getattr(module, methode)(env, response)
            #except AttributeError:
            #except TypeError:
            except:
                response("404", [("Content-type", "text/plain")])
                output = [b"Not found"]
        else:
            response("404", [("Content-type", "text/plain")])
            output = [b"Not found"]
        return(output)
if __name__ == "__main__":
    import config
    argparser = argparse.ArgumentParser(prog='gwsgi')
    argparser.add_argument("--debug", action="store_true", help="Enable more verbose logging")
    argparser.add_argument("--pidfile", action="store", help="PID file", dest="pidfile", default=config.PID_FILE)
    argparser.add_argument("--logfile", action="store", help="Log file", dest="logfile", default=config.LOG_FILE)
    args = argparser.parse_args()
    if args.debug:
        config.DEBUG = args.debug
        print("gwsgi:(%s)" % args)
    config.PID_FILE = args.pidfile
    config.LOG_FILE = args.logfile
    sys.path.insert(0, config.HTML_DIR)
    service = GWSGIServer(config)
    service.start()
    sys.exit()
