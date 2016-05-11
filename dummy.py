import cookielib
import urllib2
from lego.protocol import protocol_pb2
import time

class HttpCaller(object):
    def __init__(self):
        self.__cj = cookielib.CookieJar()
        self.__opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.__cj))

    def get(self, url):
        request = urllib2.Request(url)
        return self._request(request)

    def post(self, url, request_data):
        request = urllib2.Request(url)
        request.data = request_data
        request.headers = {"seq":1}
        return self._request(request)

    def _request(self, request):
        response = self.__opener.open(request)

        retrived_url = response.geturl()
        code = response.getcode()
        metainfo = response.info()
        body = response.read()

class Client(object):

    def __init__(self, url):
        self._httpcaller = HttpCaller()
        self.URL = url
        self._useruid = None
        self._loginid = None

def _call(self, url, request, response_type):
        q = request.SerializeToString()
        response = self._httpcaller.post(url, q)
        r = response_type()
        r.ParseFromString(response)
        return r
        

    def login(self, loginid, password):
        q = protocol_pb2.Qlogin()
        q.loginid = loginid
        q.password = password
        r = self.call(q, protocol_pb2.Rlogin)

        if r.res == 0:
            self._useruid = r.useruid
            self._loginid = loginid
            print "*** r : ", r
        else:
            raise Exception("damn", r)

    def myinfo(self):
        q = protocol_pb2.Qmyinfo()
        r = self.call(q, protocol_pb2.Rmyinfo)
        
        if r.res == 0:
            print r
            pass
        else:
            raise Exception("damn", r)

def stagelist(self):
        q = protocol_pb2.QstageList()
        q.dungeon_id = 1
        r = self.call(q, protocol_pb2.RstageList)

        if r.res == 0:
            print "r : ", r

    def entstage(self):
        q = protocol_pb2.QentStage()
        q.stage_id = 1
        q.dungeon_id = 1
        q.wallet.ink.ink_last_value = 1
        q.party.slot = 1
        q.party.lcharacteruid = 1
        q.party.p1characteruid = 2
        q.party.p2characteruid = 3

        r = self.call(q, protocol_pb2.RentStage)

        if r.res == 0:
            print "r : ", r

    def stageresult(self):
        q = protocol_pb2.QstageResult()
        q.stage_uid = 1
        q.win = 1

        r = self.call(q, protocol_pb2.RstageResult)

        print r
        #if r.res == 0:
            #print "r : ", r

    def questlist(self):
        q = protocol_pb2.QquestList()
        r = self.call(q, protocol_pb2.RquestList)

        print r

