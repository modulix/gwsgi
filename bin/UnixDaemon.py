#!/bin/env python
# -*- coding: utf-8 -*-
# (Copyleft) 2016 - AWI : Aquitaine Webmédia Indépendant
#
import sys, os, atexit
from signal import SIGTERM

class UnixDaemon(object):
    """
    Use this class to create a daemon on Unix system
    """
    def __init__(self, pidfile, logfile, errfile):
        self.pidfile = pidfile
        self.stdin = "/dev/null"
        self.stdout = logfile
        self.stderr = errfile

    def daemonize(self):
        """
        Trying a 'double-fork' as described in 'Advanced Programming in the UNIX Environment'
        """
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
        os.chdir("/")
        os.setsid()
        os.umask(0)
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
        pid = str(os.getpid())
        # PID file creation
        fd = open(self.pidfile, 'w+')
        if fd:
            fd.write("%s\n" % pid)
            fd.close()
        else:
            print("%s: PID file creation failed..." % self.pidfile)
            sys.exit(-1)
        atexit.register(self.delpid)

    def delpid(self):
        # PID file destruction
        os.remove(self.pidfile)

    def start(self, *args):
        # PID file creation
        pid = 0
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except:
            pid = None
        if pid:
            message = "%s file exist...(exiting)\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        # Starting the daemon
        self.daemonize()
        self.run(*args)
    def stop(self):
        # Read PID file
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except:
            pid = None
        if not pid:
            return
        # Kill this PID (also sometimes called Bill)
        try:
            os.kill(pid, SIGTERM)
        except:
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)
            else:
                sys.exit(1)
    def restart(self):
        self.stop()
        self.start()

    def run(self, *args):
        print("You have to override this method...")
