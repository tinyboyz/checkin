'''
Module for QQBuy credits request.

@author: leon,zhang(itasoro@gmail.com)
'''
import httplib
import json

class Credits(object):
    """constructor"""
    def __init__(self):
        self.conn = httplib.HTTPConnection("act.buy.qq.com")

    """deconstructor"""
    def __del__(self):
        self.conn.close()

    """check in for everyday"""
    def sign(self):
        self.conn.request("GET", "/landing.php?mod=checkin&act=sign")
        resp = self.conn.getresponse()
        if resp.status == 200:
            data = resp.read()
            if data:
                result = json.loads(data)
                if result["ret"] == 0:
                    BBC.jifen.indexV2.showSignTips("Ç©µ½³É¹¦",'<p class="checkin_title">ÄúÒÑÍê³É<span class="color_red">¡°Ã¿ÈÕÒ»Ç©¡±</span>²¢»ñµÃ2Íø¹º»ý·Ö½±Àø¡£<span class="checkin_title_notice">£¨×¢£º»ý·Ö½«ÓÚ24Ð¡Ê±ºóµ½ÕË£©</span></p>',"success");
                    BBC.jifen.indexV2.showQianDisabled(true);
                elif result["msg"] == "not login":
                    BBC.jifen.indexV2.setLoginCB(BBC.jifen.indexV2.signIn);
                    BBC.head.login();
                elif result["ret"] == -2012:
                    BBC.jifen.indexV2.showSignTips("Äú½ñÌìÒÑÍê³ÉÇ©µ½",'<p class="checkin_title">ÄúÒÑÍê³É<span class="color_red">¡°Ã¿ÈÕÒ»Ç©¡±</span>²¢»ñµÃ2Íø¹º»ý·Ö½±Àø£¬Ã¿ÌìÖ»ÄÜÇ©µ½Ò»´Î¡£</p>',"success");
                    BBC.jifen.indexV2.showQianDisabled(true);
                else:
                    BBC.jifen.indexV2.showSignTips("ÏµÍ³·±Ã¦",'<p class="checkin_title">ÏµÍ³·±Ã¦¡£ÇëÄúÉÔºóÔÙÊÔ</p>',"success");
                print "return:%d message:%s" % (result["ret"], result["msg"])
            else:
                print "result is null"
        else:
            print "%d %s" % (resp.status, resp.reason)