# gwsgi
WSGI Server

This Python server is designed to be run as system service with a httpd frontend.

This server, compatible with Python2 and Python3 use gevent lib.
## Installation
First, you need to copy bin directory files in a directory to which nginx have access (/var/www/bin in this doc).
### Daemon Home
    /var/www/wsgi/gwsgi.py
    /var/www/wsgi/config.py
    /var/www/wsgi/UnixDaemon.py

Edit /var/www/bin/config.py file to change parameters if needed.
### HTML_DIR
If you want to have a look on example of usage, you can copy files from html directory to your htdocs dir (/var/www/html in this doc).

    /var/www/htdocs/index.py (default site index)
    /var/www/htdocs/env.py (display env variables)
    /var/www/htdocs/exemple/* (usage exemples)

## Setup system services
### Nginx config
After, you need to add a server definition to your nginx server, have a look on contrib/nginx.conf file for example.

### Init file
You need also to create a new service init file and enable this new gwsgi service.

You can find some examples of needed files in the contrib directory.

Depending on your system you will use :

    /etc/init.d/gwsgi

or

    /usr/lib/systemd/system/gwsgi.service

## Start/Stop
Finnally, start it and begin to play...

Depending on your system services manager, launch :

    /etc/init.d/gwsgi start/stop

or

    systemctl stop/start gwsgi

