import urllib2, urllib
import time

def check_duplicate(data):
    dataValue = urllib.urlencode(data)
    request = urllib2.Request('http://127.0.0.1:8080/check_duplicate', dataValue)

    response = urllib2.urlopen(request)
    r = response.read()

    print r
    return r

def make_account(data):
    dataValue = urllib.urlencode(data)
    request = urllib2.Request('http://127.0.0.1:8080/make_account', dataValue)

    response = urllib2.urlopen(request)
    r = response.read()

    print r

def check_login(data):
    dataValue = urllib.urlencode(data)
    request = urllib2.Request('http://127.0.0.1:8080/check_login', dataValue)

    response = urllib2.urlopen(request)
    r = response.read()

    return r

def take_mydata(mycode):
    dataValue = urllib.urlencode(mycode)
    request = urllib2.Request('http://127.0.0.1:8080/get_data', dataValue)

    response = urllib2.urlopen(request)
    r = response.read()

    print r

def learn_skill(mycode):
    dataValue = urllib.urlencode(mycode)
    request = urllib2.Request('http://127.0.0.1:8080/learn_skill', dataValue)

    response = urllib2.urlopen(request)
    r = response.read()

    print r

def get_stage_list(mycode):
    dataValue = urllib.urlencode(mycode)
    request = urllib2.Request('http://127.0.0.1:8080/get_stage_list', dataValue)

    response = urllib2.urlopen(request)
    r = response.read()

    print r

def enter_stage(mycode):
    dataValue = urllib.urlencode(mycode)
    request = urllib2.Request('http://127.0.0.1:8080/enter_stage', dataValue)

    response = urllib2.urlopen(request)
    r = response.read()

    int(r)
    print 'This stage you can earn max exp:'+str(r)
    return r

def end_stage(data):
    dataValue = urllib.urlencode(data)
    request = urllib2.Request('http://127.0.0.1:8080/end_stage', dataValue)

    response = urllib2.urlopen(request)
    r = response.read()
    if r=='Error':
        print 'It cannot be saved database. try more'
    else:
        print r

def buy_item(code):
    dataValue = urllib.urlencode(code)
    request = urllib2.Request('http://127.0.0.1:8080/buy_item', dataValue)

    response = urllib2.urlopen(request)
    r = response.read()

    print r

def sell_item(code):
    dataValue = urllib.urlencode(code)
    request = urllib2.Request('http://127.0.0.1:8080/sell_item', dataValue)

    response = urllib2.urlopen(request)
    r = response.read()

    print r






def insert_data():
    print 'input your id'
    myid = raw_input()
    print 'input your passwd'
    mypw = input()
    print 'input your nickname'
    mynn = raw_input()
    data = {"user_id":myid, "user_passwd":mypw, "user_nickname":mynn}
    return data

def dupl(data):
    duplicate_result = check_duplicate(data)
    if int(duplicate_result)==0:
        print "Making account is ready!"
    else:
        print "There is already account"

def _login(data):
    login_result = check_login(data)
    if login_result==9999:
        print "Login is Error!"
    else:
        print "Login Success!"

    print login_result
    (a,b)=login_result.split('(')
    (b,c)=b.split(',')
    mycode = {"code":b}
    return mycode

def makac(data):
    make_account(data)

def main():
    while 1:
        print "1 : insert your account data \n2 : check duplicate account \n3 : login\n4 : Make Account"
        print "press key"
        prog = input()
        if prog==1:
            data = insert_data()
        elif prog==2:
            try:
                dupl(data)
            except:
                print 'there is no data input'
        elif prog==3:
            try:
                mycode = _login(data)
                selectmode(mycode)
            except:
                print 'there is no data input'
        elif prog==4:
            makac(data)
        else:
            quit()
    
def selectmode(mycode):
    while 1:
        print "1 : stage \n2 : item\n3 : skill\n4 : main"
        print "select where to go"
        prog = input()
        if prog==1:
            stage(mycode)
        elif prog==2:
            item(mycode)
        elif prog==3:
            skill(mycode)
        elif prog==4:
            main()
        else:
            quit()

def stage(mycode):
    print "taking my data\n"
    take_mydata(mycode)
    time.sleep(3)
    print "\n"
    get_stage_list(mycode)
    time.sleep(3)
    print "\n"
    enter_stage(mycode)
    time.sleep(3)
    print "\n"
    your_exp = 50
    b = mycode["code"]
    end_stage_code = {"code":b,"num":your_exp}
    end_stage(end_stage_code)
    print "\n"
    selectmode(mycode)

def skill(mycode):
    learn_skill(mycode)
    time.sleep(3)
    print "\n"
    selectmode(mycode)

def item(mycode):
    print "1: Buy\n2: Sell"
    prg = input()
    if prg==1:
        buy_item(mycode)
    elif prg==2:
        sell_item(mycode)
    elif prg==3:
        selectmode()
    else:
        quit()

main()
