#!/usr/bin/python
"""
    CheckIn
    Copyright (C) 2013  Lei Zhang(itasoro@gmail.com)

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
from datetime import timedelta
from datetime import datetime
import signal
from threading import Event
import struct
import time
import yaml
from random import randint
from random import random
from taobao import Taobao
from daemon import Daemon
from apscheduler.scheduler import Scheduler

stopevent = Event()


class Main(Daemon):
    """
    do some things
    """
    def __init__(self, pidfile, cfgfile):
        Daemon.__init__(self, pidfile)
        self.jobs = {}
        self.immediately = False
        self.scheduler = Scheduler(daemonic=False)
        self.logger = logging.getLogger(self.__class__.__name__)
        if os.path.exists(cfgfile):
            with open(cfgfile, 'rt') as f:
                config = yaml.load(f.read())
            for k1 in config.keys():
                if k1 == 'version':
                    pass
                if k1 == 'immediately':
                    self.immediately = config[k1]
                elif k1 == 'taobao':
                    self.jobs[k1] = config[k1]
                    self.jobs[k1]['id'] = None
                    if 'chktime' in self.jobs[k1].keys():
                        self.jobs[k1]['btime'] = time.strptime(self.jobs[k1]['chktime'].split('-')[0], '%H:%M')
                        self.jobs[k1]['etime'] = time.strptime(self.jobs[k1]['chktime'].split('-')[1], '%H:%M')
                        if self.jobs[k1]['btime'] >= self.jobs[k1]['etime']:
                            raise ValueError('"chktime" is illegal')
                    else:
                        raise ValueError('There is no "chktime" be found in configure.')
                else:
                    pass
        else:
            self.logger.error('{0} not found'.format(cfgfile))

    def job_main(self):
        st_beg = self.jobs['taobao']['btime']
        st_end = self.jobs['taobao']['etime']
        dt_beg = datetime.now().replace(hour=st_beg.tm_hour, minute=st_beg.tm_min)
        dt_end = datetime.now().replace(hour=st_end.tm_hour, minute=st_end.tm_min)
        td_rnd = dt_end - dt_beg
        dt_rnd = dt_beg + timedelta(seconds=randint(1, td_rnd.days * 86400 + td_rnd.seconds - 1))
        if dt_rnd <= datetime.now():
            dt_rnd += timedelta(days=1)
        self.jobs['taobao']['id'] = self.scheduler.add_date_job(lambda: self.job_taobao(), dt_rnd)

    def job_taobao(self):
        for v in self.jobs['taobao']['account']:
            taobao = Taobao(v['username'], v['password'])
            if taobao.login():
                taobao.checkin()

    def run(self):
        if self.immediately:
            self.job_taobao()
            self.immediately = False
        self.scheduler.add_cron_job(lambda: self.job_main(), hour='0', minute='1')
        self.scheduler.start()
        stopevent.wait()
        self.scheduler.shutdown()


def showhelp():
    print 'usage: python checkin.py start | stop | restart | nodaemon'


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
    try:
        daemon = Main('/var/run/checkin.pid', 'checkin.yaml')
    except ValueError as ex:
        logger.error(ex)
        sys.exit(-1)
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