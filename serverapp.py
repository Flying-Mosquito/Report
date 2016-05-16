from bottle import run, route, request, post
import MySQLdb
import json      
import mquery

class ServerApp(object):
    def __init__(self):
        print 'ServerApp Init success'

        _host = "127.0.0.1"
        _port = 3306
        _dbuser = "root"
        _dbpassword = "thdud12"
        _dbname = "mosquito"

        self.db = MySQLdb.connect(host=_host, port=_port, user=_dbuser, passwd=_dbpassword, db=_dbname)

    def run(self):
        print 'Web Server is Starting!'
        myiphost = "127.0.0.1"
        run(host=myiphost, port=8080, debug=True)

    def make_account(self, req):
        user_id = req.forms.get('user_id')
        user_passwd = req.forms.get('user_passwd')
        user_nickname = req.forms.get('user_nickname')
        
        print 'Making new account'
        cursor = self.db.cursor()
        cursor.execute(mquery.init_account_query,(user_id,user_passwd,user_nickname))
        print 'init user columns is success'
        cursor.execute(mquery.get_useruid_query,(user_id))
        res = cursor.fetchall()
        for r in res:
            a = r[0]
            
        cursor.execute(mquery.init_skill_query,(a))
        print 'init skill columns is success'
        cursor.execute(mquery.init_ranking_query,(a,0,1))
        print 'init ranking columns is success'
        cursor.execute(mquery.init_item_query,(a,0,0,0,0,0,0,0,0,0))
        print 'init items columns is success'
        cursor.execute('insert into stage values(%s,1)',(a))

    def check_duplicate(self,req):
        user_id = req.forms.get('user_id')
        user_nickname = req.forms.get('user_nickname')
        print 'Checking duplicate nickname, userid!'
        cursor = self.db.cursor()
        un_correct = cursor.execute(mquery.check_duplicate_username_query,(user_id))
        nn_correct = cursor.execute(mquery.check_duplicate_nickname_query,(user_nickname))
        if un_correct == 1:
            if nn_correct == 1:
                return 1
            else:
                return 0
        else:
            return 0

    def check_login(self,req):
        user_name = req.forms.get('user_id')
        user_passwd = req.forms.get('user_passwd')
        cursor = self.db.cursor()
        ck = cursor.execute(mquery.get_passwd_query,(user_name))
        if ck == 1:
            cursor.execute(mquery.get_useruid_query,(user_name))
            ud = cursor.fetchall()
            return ud[0]
        else:
            erlog = 9999
            return erlog

    def get_user_level(self,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        cursor.execute(mquery.get_level_query,(user_uid))
        results = cursor.fetchall()
        return results[0]

    def get_user_exp(self,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        cursor.execute(mquery.get_exp_query,(user_uid))
        results = cursor.fetchall()
        return results[0]

    def get_user_money(self,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        cursor.execute(mquery.get_money_query,(user_uid))
        results = cursor.fetchall()
        return results[0]

    def get_user_score(self,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        cursor.execute(mquery.get_score_query,(user_uid))
        results = cursor.fetchall()
        return results[0]

    def skill_level(self,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        cursor.execute(mquery.get_skill_level_query,(user_uid))
        results = cursor.fetchall()
        return results[0]

    def skill_cost(self,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        cursor.execute(mquery.get_skill_cost_query,(user_uid))
        results = cursor.fetchall()
        return results[0]

    def get_ranking_db(self,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        cursor.execute(mquery.get_ranking_query,(user_uid))
        results = cursor.fetchall()
        return results

    def get_item_num(self,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        cursor.execute(mquery.get_item_num_query,(user_uid))
        results = cursor.fetchall()
        return results

    def get_item_type(self,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        cursor.execute(mquery.get_item_type_query,(user_uid))
        results = cursor.fetchall()
        return results

    def get_item_id(self,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        cursor.execute(mquery.get_item_id_query,(user_uid))
        results = cursor.fetchall()
        return results

    def get_stage_list(self,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        cursor.execute('select progress from stage where stage_useruid=%s',(user_uid))
        results = cursor.fetchall()
        return results[0]

    def update_stage_list(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        r = cursor.execute('update stage set progress=progress+%s where stage_useruid=%s',(num,user_uid))
        return r
    
    def modify_level(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(modify_level_query,(num,user_uid))
        return result

    def modify_exp(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(modify_exp_query,(num,user_uid))
        return result

    def modify_money(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.modify_money_query,(num,user_uid))
        return result

    def modify_score(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(modify_money_query,(num,user_uid))
        return result

    def modify_skill_level(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(modify_skill_level_query,(num,user_uid))
        return result

    def modify_skill_level2(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(modify_skill_level2_query,(num,user_uid))
        return result

    def modify_skill_level3(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(modify_skill_level3_query,(num,user_uid))
        return result

    def modify_skill_cost(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(modify_skill_cost_query,(num,user_uid))
        return result

    def modify_skill_cost2(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(modify_skill_cost2_query,(num,user_uid))
        return result

    def modify_skill_cost3(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(modify_skill_cost3_query,(num,user_uid))
        return result

    def modify_item_id(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.modify_item_id_query,(num,user_uid))
        return result

    def modify_item_id2(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.modify_item_id2_query,(num,user_uid))
        return result

    def modify_item_id3(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.modify_item_id3_query,(num,user_uid))
        return result

    def modify_item_type(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.modify_item_type_query,(num,user_uid))
        return result

    def modify_item_type2(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.modify_item_type2_query,(num,user_uid))
        return result

    def modify_item_type3(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.modify_item_type3_query,(num,user_uid))
        return result

    def user_update_level(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(user_update_level_query,(num,user_uid))
        return result

    def user_update_exp(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.user_update_exp_query,(num,user_uid))
        return result

    def user_update_money(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        num = num * 10
        cursor = self.db.cursor()
        result = cursor.execute(mquery.user_update_money_query,(num,user_uid))
        return result

    def user_update_score(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        num = num+123
        cursor = self.db.cursor()
        result = cursor.execute(mquery.user_update_score_query,(num,user_uid))
        return result

    def update_skill_level(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.update_skill_level_query,(num,user_uid))
        return result

    def update_skill_level2(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(update_skill_level2_query,(num,user_uid))
        return result

    def update_skill_level3(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(update_skill_level3_query,(num,user_uid))
        return result

    def update_skill_cost(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.update_skill_cost_query,(num,user_uid))
        return result

    def update_skill_cost2(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(update_skill_cost2_query,(num,user_uid))
        return result

    def update_skill_cost3(self,num,user_uid):
        cursor = self.db.cursor()
        result = cursor.execute(update_skill_cost3_query,(num,user_uid))
        return result

    def update_item_num(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.update_item_num_query,(num,user_uid))
        return result

    def update_item_num2(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.update_item_num2_query,(num,user_uid))
        return result

    def update_item_num3(self,num,req):
        user_uid = req.forms.get('code')
        user_uid = long(user_uid)
        cursor = self.db.cursor()
        result = cursor.execute(mquery.update_item_num3_query,(num,user_uid))
        return result


