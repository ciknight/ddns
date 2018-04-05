# -*- coding: utf-8 -*-
'''
    ***
    Modified generic daemon class
    ***

    Author:     http://www.jejik.com/articles/2007/02/a_simple_unix_linux_daemon_in_python/
                www.boxedice.com

    License:    http://creativecommons.org/licenses/by-sa/3.0/

    Changes:    23rd Jan 2009 (David Mytton <david@boxedice.com>)
                - Replaced hard coded '/dev/null in __init__ with os.devnull
                - Added OS check to conditionally remove code that doesn't work on OS X
                - Added output to console on completion
                - Tidied up formatting
                11th Mar 2009 (David Mytton <david@boxedice.com>)
                - Fixed problem with daemon exiting on Python 2.4 (before SystemExit was part of the Exception base)
                13th Aug 2010 (David Mytton <david@boxedice.com>
                - Fixed unhandled exception if PID file is empty
'''

import atexit
import os
import signal
import sys
import time

from util.logger import getLogger

logger = getLogger(__name__)


class Daemon():
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin=os.devnull, stdout=os.devnull,
                 stderr=os.devnull, home_dir='.', umask='022', verbose=1):
        super().__init__()
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.home_dir = home_dir
        self.verbose = verbose
        self.umask = umask
        self.daemon_alive = True

    def daemonize(self):
        """
        Do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # Exit from second parent
                sys.exit(0)
        except OSError:
            self.log('error', 'form #2 faild')
            sys.exit(1)
        # if sys.platform != 'darwin':    # This block breaks on OS X
        #     # Redirect standard file descriptions
        #     sys.stdout.flush()
        #     sys.stderr.flush()
        #     si = open(self.stdin, 'r')
        #     so = open(self.stdout, 'a+')
        #     if self.stderr:
        #         se = open(self.stderr, 'a+')
        #     else:
        #         se = so
        #     os.dup2(si.fileno(), sys.stdin.fileno())
        #     os.dup2(so.fileno(), sys.stdout.fileno())
        #     os.dup2(se.fileno(), sys.stderr.fileno())

        def sigtermhandler(signum, frame):
            self.daemon_alive = False

        signal.signal(signal.SIGTERM, sigtermhandler)
        signal.signal(signal.SIGINT, sigtermhandler)
        self.log('success', 'Started, server is running')

        # Write pidfile
        atexit.register(self.delpid)    # Make sure pid file removed if we quite
        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as f:
            f.write('{}'.format(pid))

    def delpid(self):
        os.remove(self.pidfile)

    def log(self, status='info', s=''):
        if not s: return
        if self.verbose >= 1:
            try:
                log = logger.__getattribute__(status)
            except Exception:
                self.log.error('logger not have attribute {}'.format(status))
            log(s)
        return

    def start(self, *args, **kwargs):
        """
        running daemon
        """
        self.log('info', 'Starting daemon...')
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
        except ValueError:
            pid = None
        if pid:
            message = 'pidfile {} already exists. it is already running?'.format(self.pidfile)
            self.log('warning', message)
            sys.exit(0)

        # Start the daemon
        self.daemonize()
        self.run(*args, **kwargs)

    def stop(self):
        """
        Stop the daemon
        """
        self.log('info', 'Stoping daemon...')
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None
        except ValueError:
            pid = None

        if not pid:
            message = "pidfile {} does not exist. Not running?".format(self.pidfile)
            self.log('warning', message)

            # Just to be sure. A ValueError might occur if the PID file is empty but does actually exist
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)

            return    # Not an error in a restart

        # Try killing the daemon process
        try:
            i = 0
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
                i += 1
                if i % 10 == 0:
                    os.kill(pid, signal.SIGHUP)
        except OSError as e:
            err = str(e)
            if err.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                self.log('error', err)
                sys.exit(1)

        self.log('success', 'Stopped')

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def status(self):
        """
        Report daemon status
        """
        try:
            with open(self.pidfile, 'r') as f:
                pid = int(f.read().strip())
        except IOError:
            pid = None
        except SystemExit:
            pid = None

        if pid:
            self.log('info', 'Running')
        else:
            self.log('info', 'Stopped')

    def run(self, *args, **kwargs):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """
        del args, kwargs
