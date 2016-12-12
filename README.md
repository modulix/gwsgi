# gwsgi
WSGI Server

This Python server is designed to be run as system service with a httpd frontend.

This server is compatible with Python2 and Python3 and use gevent lib.
## Installation
    git clone https://github.com/modulix/gwsgi .
	cp -r gwsgi/bin/* /var/www/bin/
### Daemon Home
    /var/www/bin/gwsgi.py (wsgi server)
    /var/www/bin/config.py (configuration file)
    /var/www/bin/UnixDaemon.py (Python class to run gwsgi.py as system service)

Review /var/www/bin/config.py file and change parameters if needed.

If you want to have a look on example of usage, you can copy files from html directory to your htdocs dir (/var/www/html in this doc).

	cp -r gwsgi/html/* /var/www/html/
### HTML_DIR
    /var/www/htdocs/index.py (default site index)
    /var/www/htdocs/example/* (usage examples)
    /var/www/htdocs/example/env.py (display env variables)
    /var/www/htdocs/example/jinja.py (use template with jinja)

## Setup system services
### httpd config
After, you need to add a server definition to your httpd server, have a look on contrib directory for examples.

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

