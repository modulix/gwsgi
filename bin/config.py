#!/bin/env python
# -*- coding: utf-8 -*-
# GWSGI : Configuration file
#
SERVER = "127.0.0.1"
PORT = 8888
MAX_CLIENTS = 1024
HTML_DIR = "/var/www/html"
PID_FILE="/run/gwsgi.pid"
ERR_FILE="/var/log/gwsgi/error.log"
LOG_FILE="/var/log/gwsgi/access.log"
LOG_FORMAT="%(asctime)s [%(levelname)s] %(name)s %(message)s"
# DEFAULT_INDEX is DefaultPythonFilenameWithoutPyExtension.DefaultResponseMimeType
DEFAULT_INDEX = "index.html"
DEFAULT_METHOD = "index"
DEBUG = False
