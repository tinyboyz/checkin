#!/usr/bin/python
"""
    CheckIn
    Copyright (C) 2013  Leon(itasoro@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
import logging
import logging.config
import signal
from threading import Event
import yaml
from random import randint
from taobao import Taobao
from daemon import Daemon
from apscheduler.scheduler import Scheduler

stopevent = Event()

class Main(Daemon):
    """
    do some things
    """
    def __init__(self, pidfile):
        Daemon.__init__(self, pidfile)
        self.sched_master = Scheduler(daemonic=False)
        self.taobao_job = None
        self.checkin_conf = 'checkin.yaml'
        self.logger = logging.getLogger(self.__class__.__name__)
        self.taobao_account = {}
        if os.path.exists(self.checkin_conf):
            with open(self.checkin_conf, 'rt') as f:
                self.config = yaml.load(f.read())
        else:
            self.logger.error('checkin.yaml not found')
        if self.config and 'website' in self.config.keys():
            if self.config['website']:
                if 'taobao' in self.config['website'].keys():
                    self.taobao_account = self.config['website']['taobao']
                if 'qqbuy' in self.config['website'].keys():
                    self.qqbuy_account = self.config['website']['qqbuy']

    def scheduler_job(self):
        self.taobao_job = self.sched_master.add_cron_job(lambda: self.taobao_jobs(), hour='{0}'.format(randint(9, 18)),
                                                         minute='{0}'.format(randint(1, 59)))

    def taobao_jobs(self):
        self.sched_master.unschedule_job(self.taobao_job)
        for k, v in self.taobao_account.iteritems():
            taobao = Taobao(v['username'], v['password'])
            if taobao.login():
               taobao.checkin()

    def run(self):
        self.sched_master.add_cron_job(lambda: self.scheduler_job(), hour='8', minute='50')
        self.sched_master.start()
        stopevent.wait()
        self.sched_master.shutdown()

def showhelp():
    print "usage: python checkin.py start|stop|restart|nodaemon"

def sigterm_handler(signum, frame):
    logging.info('capture {0} signal'.format(signum))
    stopevent.set()

if __name__ == '__main__':
    # handle special signal for stopping
    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigterm_handler)
    # configure logging
    logging_conf = 'logging.yaml'
    if os.path.exists(logging_conf):
        with open(logging_conf, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    daemon = Main('/var/run/checkin.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            logger.info('checkin started')
            daemon.start()
        elif 'stop' == sys.argv[1]:
            logger.info('checkin stopped')
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            logger.info('checkin restarted')
            daemon.restart()
        elif 'nodaemon' == sys.argv[1]:
            logger.info('checkin started for debuging')
            daemon.run()
        else:
            showhelp()
    else:
        showhelp()
    sys.exit(0)