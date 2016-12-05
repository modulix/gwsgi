# gwsgi
WSGI Server

This Python server is designed to be run as system service and with Nginx frontend.
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
### Nginx config
After, you need to add a server definition to your nginx server :

(todo)

### Init file
Finnally, create a new service init file, enable gwsgi service, start it and play...

You can find some examples of needed files in the contrib directory.

Depending on your system you will need :

/etc/init.d/gwsgi

or

/usr/lib/systemd/system/gwsgi.service
## Start/Stop
Use your system service manager :
/etc/init.d/gwsgi start/stop

or

systemctl stop/sart gwsgi

