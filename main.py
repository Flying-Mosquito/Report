from serverapp import ServerApp
from bottle import request, post, route, get, response

serverapp = ServerApp()
@post('/make_account')
def make_account():
    req = request
    r = serverapp.check_duplicate(req)
    if r==0:
        serverapp.make_account(req)
        return "making account OK"
    else:
        return "There is already account!"

@post('/check_duplicate')
def check_duplicate():
    req = request
    r = serverapp.check_duplicate(req)
    if r == 1:
        return "1"
    else:
        return "0"

@post('/check_login')
def check_login():
    req = request
    r = serverapp.check_login(req)
    if r == 9999:
        return "Error"
    else:
        return str(r)
    
@post('/get_data')
def get_data():
    req = request
    r = serverapp.get_user_level(req)
    s = serverapp.get_user_exp(req)
    m = serverapp.get_user_money(req)
    j = serverapp.get_user_score(req)
    mess = 'level:'+str(r) +', exp:'+str(s)+', money:'+str(m)+', score:'+str(j)
    return mess

@post('/get_stage_list')
def get_stage_list():
    req = request
    r = serverapp.get_stage_list(req)
    mess = 'Can enter stage level now:' +str(r)
    return mess

@post('/enter_stage')
def enter_stage():
    req = request
    r = serverapp.get_stage_list(req)
    can_exp = r[0] * 100
    return str(can_exp)

@post('/end_stage')
def end_stage():
    req = request
    r = serverapp.get_stage_list(req)
    can_exp = r[0] * 100
    earn_exp = req.forms.get('num')
    earn_exp = long(earn_exp)

    if can_exp >= earn_exp:
        serverapp.user_update_exp(earn_exp,req)
        serverapp.user_update_score(earn_exp,req)
        serverapp.user_update_money(earn_exp,req)
        e = serverapp.get_user_exp(req)
        m = serverapp.get_user_money(req)
        s = serverapp.get_user_score(req)
        serverapp.update_stage_list(1,req)
        gs = serverapp.get_stage_list(req)
        mess = 'Now Exp:'+str(e)+' Money:'+str(e)+' Score:'+str(s)+' Stage:'+str(gs)
        return mess
    else:
        return 'Error'
    

@post('/learn_skill')
def learn_skill():
    req = request
    mon = serverapp.get_user_money(req)
    skc = serverapp.skill_cost(req)
    mon = mon[0]
    skc = skc[0]
    
    if skc > mon:
        return 'You cannot learn skill, please earn more money'
    else:
        serverapp.update_skill_level(1,req)
        serverapp.update_skill_cost(500,req)
        rem = mon - skc
        serverapp.modify_money(rem,req)
        sklev = serverapp.skill_level(req)
        skcost = serverapp.skill_cost(req)
        sklev = sklev[0]
        skcost = skcost[0]
        mess = 'Now your skill level:'+str(sklev)+' Skill cost:'+str(skcost)+' Money:'+str(rem)
        return mess

@post('/buy_item')
def buy_item():
    req = request

    serverapp.modify_item_id(1,req)
    serverapp.modify_item_type(1,req)

    mon =serverapp.get_user_money(req)
    mon = mon[0]
    if mon > 100:
        serverapp.update_item_num(1,req)
        mon = mon-100
        serverapp.modify_money(mon,req)
        itm = serverapp.get_item_num(req)
        m = itm[0]
        typ = serverapp.get_item_type(req)
        typ = typ[0]
        mess = 'Now your non-equipment type item amount is:'+str(m[0])+' Money:'+str(mon)
        return mess
    else:
        return 'Not enough your money'
    
@post('/sell_item')
def sell_item():
    req = request

    itm = serverapp.get_item_num(req)
    itm = itm[0]

    if itm > 0:
        serverapp.update_item_num(-1,req)
        serverapp.user_update_money(50,req)
        mon = serverapp.get_user_money(req)
        mon = mon[0]
        mess = 'Now, your item amount is:'+str(itm)+' and your money:'+str(mon)
        return mess
    else:
        return 'You have not enough item amount'



serverapp.run() 

