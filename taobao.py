"""
    CheckIn
    Copyright (C) 2013 Lei Zhang(itasoro@gmail.com)

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
import httplib
import urllib
import json
import requests
import pprint
import time
import re
import json
import logging

class Taobao(object):
    """
    logon the web site(www.taobao.com) for checking in
    """

    def __init__(self, username, password):
        """
        constructor
        """
        self.session = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tips1 = '[taobao][{0}]Success!Obain {1} gold in {2} days.Current Gold:{3},Tomorrow Gold:{4}.'
        self.tips2 = '[taobao][{0}]Already Checked In!'
        self.tips4 = '[taobao][{0}]Need Verification Code!'
        self.tips5 = '[taobao][{0}]Verification Code Is Wrong!'
        self.tips6 = '[taobao][{0}]You Need 5 Friends At Least For Gold!'
        self.username = username
        self.password = password
        self.login_token = ''
        self.login_url = 'https://login.taobao.com/member/login.jhtml'
        self.taogold_url = 'http://vip.taobao.com/home/grant_everyday_coin.htm?t={0}&_tb_token_={1}&checkCode=null' \
                           '&enter_time={2}'

    def __del__(self):
        """
        destructor
        """
        pass

    def login(self):
        """
        login from taobao.com
        """
        login_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                         'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; '
                                       '.NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; '
                                       'Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.2; Tablet PC 2.0)',
                         'Host': 'login.taobao.com'}
        params = {'TPL_username': self.username, 'TPL_password': self.password}
        try:
            self.session = requests.Session()
            response1 = self.session.post(self.login_url, data=params, headers=login_headers, allow_redirects=True)
            if response1.status_code == 200:
                # get redirect url
                matchs = re.search('window.location = \"(.*)\";', response1.content)
                if matchs:
                    redirected_url = matchs.group(1)
                    response2 = self.session.get(redirected_url)
                    if response2.status_code == 200:
                        if '_tb_token_' in response2.cookies.keys():
                            self.login_token = response2.cookies['_tb_token_']
                        else:
                            self.logger.error('_tb_token_ is not in cookies')
                            return False
                        return True
                    else:
                        self.logger.error('get {0} failed,{1}'.format(redirected_url, response2.status_code))
                else:
                    self.logger.error('redirect url is null')
            else:
                self.logger.error('post {0} failed,{1}'.format((self.login_url, response1.status_code)))
        except requests.exceptions as e:
            self.logger.error('request exceptions,{0}' % e.strerror)
        except re.error as e:
            self.logger.error('regularity expression error,{0}'.format(e.strerror))
        return False

    def checkin(self):
        """ obtain taobao gold """
        curtime_ms = time.time() * 1000
        t = curtime_ms - 12345
        taogold_url = self.taogold_url.format(t, self.login_token, curtime_ms)
        try:
            response = self.session.get(taogold_url)
            if response.status_code == 200:
                response_json = response.json()
                code = response_json['code']
                persitent_days = response_json['daysTomorrow']
                gold_tom = response_json['coinTomorrow']
                gold_cur = response_json['coinNew']
                gold_pre = response_json['coinOld']
                if code == 1:
                    self.logger.info(self.tips1.format(self.username, gold_cur - gold_pre, persitent_days, gold_cur,
                                                       gold_tom))
                elif code == 2:
                    self.logger.warn(self.tips2.format(self.username))
                elif code == 4:
                    self.logger.warn(self.tips4.format(self.username))
                elif code == 5:
                    self.logger.warn(self.tips5.format(self.username))
                elif code == 6:
                    self.logger.warn(self.tips6.format(self.username))
                else:
                    self.logger.warn('unknown code in code list')
            else:
                self.logger.error('get {0} failed,{1}'.format((taogold_url, response.status_code)))
        except requests.exceptions as e:
            self.logger.error('request exceptions,{0}' % e.strerror)
        except KeyError as e:
            self.logger.error('keyerror,{0}' % e.strerror)
        return False