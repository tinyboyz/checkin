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
import httplib, urllib, json

class Taobao(object):
    """
    logon the web site(www.taobao.com) for checking in
    """

    def __init__(self, username, password):
        """
        constructor
        """
        self.username = username
        self.password = password
        self.login_url = 'login.taobao.com'
        self.login_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                              'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.2; Tablet PC 2.0)',
                              'Host': 'login.taobao.com'}

    def __del__(self):
        """
        destructor
        """
        pass

    def login(self):
        """
        login from taobao.com
        """
        params = urllib.urlencode({'@TPL_username': self.username, '@TPL_password': self.password})
        try:
            loginRequest = httplib.HTTPConnection(self.login_url, 80)
            loginRequest.request('POST', '/member/login.jhtml', params, self.login_headers)
            response = loginRequest.getresponse()
            if response.status == 302:
                """ get redirect url """
                location = response.getheader('Location')
                print location
                data = response.read()
                if data:
                    print data
                    # result = json.loads(data)
                else:
                    print "result is null"
            else:
                print "%d %s" % (response.status, response.reason)
            loginRequest.close()
        except httplib.HTTPException:
            print ""
        except httplib.HTTPException:
            print ""
        except httplib.NotConnected:
            print ""
        except httplib.InvalidURL:
            print ""
        except httplib.UnknownProtocol:
            print ""
        except httplib.UnknownTransferEncoding:
            print ""
        except httplib.UnimplementedFileMode:
            print ""
        except httplib.IncompleteRead:
            print ""
        except httplib.ImproperConnectionState:
            print ""
        except httplib.CannotSendRequest:
            print ""
        except httplib.CannotSendHeader:
            print ""
        except httplib.ResponseNotReady:
            print ""
        except httplib.BadStatusLine:
            print ""
