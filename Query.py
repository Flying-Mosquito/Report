# -*- coding: utf-8 -*-

# ----- ���� ����
get_useruid_nickname_query = "select useruid, nickname from  user where useruid=%s"
check_duplicate_nickname_query = "select nickname from user where nickname=%s"

get_user_friend_list_query = "select useruid2 from user_relation where useruid1=%s and status=%s limit 50"
get_user_friend_info_query = "select useruid, nickname, lcharacter_id, UNIX_TIMESTAMP(lastlogin), lcharacteruid from user where useruid=%s"
get_account_query = "select useruid from account where useruid=%s "
get_check_friend_list_query = "select count(useruid2) from user_relation where useruid1=%s and status=%s"
get_check_already_query = "select status from user_relation where (useruid1=%s and useruid2=%s) and status=%s"
get_check_friend_invite_query = "select status from invite_friend where invite_useruid=%s and accept_useruid=%s"
get_check_max_friend_invite_query = "select count(invite_useruid) from invite_friend where accept_useruid=%s and status=%s"
insert_invitefriend_list_query = ("insert into "
                                  "invite_friend(invite_useruid, accept_useruid, status) "
                                  "values(%s,%s,%s)")
insert_friend_query = ("insert into user_relation(useruid1, useruid2, ctime, status) "
                       "values(%s,%s,now(),%s),(%s,%s,now(),%s) "
                       "on duplicate key update status=%s")
delete_invite_friend_query = "delete from invite_friend where invite_useruid=%s and accept_useruid=%s and status=%s" 
get_invite_friend_list_query = "select invite_useruid from invite_friend where accept_useruid=%s and status=%s limit 30"
update_friend_query = ("update user_relation "
                       "set status=%s where useruid1=%s and useruid2=%s or "
                       "useruid1=%s and useruid2=%s and status=%s")
get_check_delete_count_query = "select unix_timestamp(friend_delete_time), friend_delete_count from user where useruid=%s"
update_delete_friend_and_count_query = ("update user set "
                                        "friend_delete_time=from_unixtime(%s), friend_delete_count=1 "
                                        "where useruid=%s")
update_delete_friend_count_query = ("update user set "
                                    "friend_delete_count=friend_delete_count+1 "
                                    "where useruid=%s")
get_friend_level_query = "select level from user_character where useruid=%s and characteruid=%s"
get_support_time_query = "select support_useruid, UNIX_TIMESTAMP(support_endtime) from user_support where useruid=%s"
get_userinfo_by_nickname_query = ("select useruid, nickname, lcharacter_id, "
                                  "UNIX_TIMESTAMP(lastlogin), lcharacteruid "
                                  "from user where nickname=%s")
get_new_friend_query = "select useruid2 from user_relation where useruid1=%s and status=%s and new_check=%s limit 50"
update_new_check_friend_query = "update user_relation set new_check=%s where useruid1=%s"
get_new_invite_friend_list_query = "select invite_useruid from invite_friend where accept_useruid=%s and status=%s and new_check=%s limit 30"
update_new_check_invite_friend_query = "update invite_friend set new_check=%s where accept_useruid=%s"
get_send_fp_endtime_query = "select UNIX_TIMESTAMP(send_fptime) from user_relation where useruid1=%s and useruid2=%s and status=%s"
update_send_fp_endtime_query = "update user_relation set send_fptime=from_unixtime(%s) where useruid1=%s and useruid2=%s and status=%s"
get_character_id_and_level_query = "select character_id, level, weapon_id from user_character where useruid={0} and characteruid in ({1})"
remove_all_friend_query = "delete from user_relation where useruid1=%s or useruid2=%s"
remove_all_invite_friend_query ="delete from invite_friend where invite_useruid=%s or accept_useruid=%s"

quest_info_query = 'select quest_id, count, status from user_quest where useruid=%s and quest_id=%s'
quest_list_info_query = 'select quest_id, count, status from user_quest where useruid=%s and quest_subtype=%s and status in ({0})'.format("{quest_status_list}")

quest_all_info_query = 'select quest_id, count, status from user_quest where useruid=%s'
quest_reward_object_query = 'select quest_id, count, status from user_quest where useruid=%s and status=%s'

modify_quest_query = ('insert into user_quest'
                     '(useruid, quest_id, quest_subtype, count, status) '
                     'values(%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE '
                     'count=%s, status=%s')

# ------ /���� ����

# ���ӿ� ���� �� �������� Ȯ��
def get_useruid_nickname_db(db, useruid, nickname):
    account_rs = db.query(get_useruid_nickname_query, (useruid,))
    return account_rs

# �г��� �ߺ� üũ
def check_duplicate_nickname_db(db, nickname):
    nick_rs = db.query(check_duplicate_nickname_query, (nickname,))
    return nick_rs

# -- ������ ģ������ �о�´�.
def get_user_friend_list_db(db, useruid, status):
    rs = db.query(get_user_friend_list_query, (useruid, status))
    # �ű������̰ų� ģ���� ���� ������� rs�� None�̶� ������ �ƴϴ�.
    return [x[0] for x in rs]

# -- ģ���� ������ �о�´�.
def get_user_friend_info_db(db, useruid):
    rs = db.query(get_user_friend_info_query, (useruid,))
    if not rs:
        raise DBAccessError("get_user_friend_info_db error", useruid=useruid)

    return rs[0]

def get_friend_level_db(db, useruid, lcharacteruid):
    rs = db.query(get_friend_level_query, (useruid, lcharacteruid))
    if not rs:
        raise DBAccessError("get_friend_level_db error", useruid=useruid,lcharacteruid=lcharacteruid)
    
    return rs[0]

# -- ���Ե� �����ΰ� �˻�
def get_account_db(db, useruid):
    rs = db.query(get_account_query, (useruid,))
    if not rs:
        raise DBAccessError("get_account_db error, useruid could not be found", useruid=useruid)

# -- ���� ģ�� ����Ʈ MAX Ȯ��
# -- ���� ģ�� ���� ��� ����Ʈ MAX Ȯ��
# status = 10 -> ģ�� ����Ʈ, status = 11 -> ���� ��� ����Ʈ
def get_check_friend_list_db(db, useruid, status):
    rs = db.query(get_check_friend_list_query, (useruid, status))
    return rs[0][0]

# -- ���� ģ�� ���� Ȯ��
# ���� �̹� ģ�� �������� Ȯ��
def get_check_already_db(db, useruid1, useruid2, status):
    rs = db.query(get_check_already_query,(useruid1, useruid2, status))
    return rs

# -- ���� ģ�� ���� ����Ʈ Ȯ��
# �̹� ģ�� ��û �������� Ȯ��
def get_check_friend_invite_db(db, invite_useruid, accept_useruid):
    rs = db.query(get_check_friend_invite_query, (invite_useruid, accept_useruid))
    return rs

# -- ���� ģ�� ���� ����Ʈ MAX Ȯ��
def get_check_max_friend_invite_db(db, accept_useruid, status):
    rs = db.query(get_check_max_friend_invite_query, (accept_useruid, status))
    return rs[0][0]

# -- ģ�� ���� ��� ����Ʈ ���
def insert_invitefriend_list_db(db, invite_useruid, accept_useruid, status):
    db.execute(insert_invitefriend_list_query, (invite_useruid, accept_useruid, status))

# -- ģ�� ����Ʈ ���
def insert_friend_db(db, useruid1, useruid2, status):
    db.execute(insert_friend_query, (useruid1, useruid2, status, useruid2, useruid1, status , status))

# -- ģ�� ���� ���·� ����
def update_erase_friend_db(db, useruid1, useruid2, invite_status, erase_status):
    db.execute(update_friend_query, (erase_status, useruid1, useruid2, useruid2, useruid1, invite_status))

# -- ģ�� ���� ��� ����Ʈ ����
def delete_invite_friend_db(db, invite_useruid, accept_useruid, status):
    db.execute(delete_invite_friend_query, (invite_useruid, accept_useruid, status))

# -- ģ�� ���� ��� ����Ʈ �ҷ�����
def get_invite_friend_list_db(db, useruid, status):
    rs = db.query(get_invite_friend_list_query, (useruid, status))
    # �ű������̰ų� ģ���� ���� ������� rs�� None�̶� ������ �ƴϴ�.
    return [x[0] for x in rs]

# -- �г������� �˻�
def get_userinfo_by_nickname_db(db, nickname):
    rs = db.query(get_userinfo_by_nickname_query, (u"{0}".format(nickname),))
    return rs

# -- �� ģ�� ��û �˻�
def get_new_invite_friend_list_db(db, useruid, status, check_status):
    rs = db.query(get_new_invite_friend_list_query, (useruid, status, check_status))
    return [x[0] for x in rs]

# -- ģ�� ��û new_check ���¸� 0���� ������Ʈ
def update_new_check_invite_friend_db(db, useruid, check_status):
    db.execute(update_new_check_invite_friend_query, (check_status, useruid))

# -- �� ģ�� �˻�
def get_new_friend_db(db, useruid, status, check_status):
    rs = db.query(get_new_friend_query, (useruid, status, check_status))
    return [x[0] for x in rs]

# -- ģ�� new_check ���� 0���� ������Ʈ
def update_new_check_friend_db(db, useruid, check_status):
    db.execute(update_new_check_friend_query, (check_status, useruid))

# -- Ż���� ������ ��� ģ�� ����
def remove_all_friend_db(db, useruid):
    db.execute(remove_all_friend_query, (useruid, useruid))

# -- Ż���� ������ ������⸮��Ʈ ���� �� Ż�� ������ ��û�� ģ�� ���� ��û ����
def remove_all_invite_friend_db(db, useruid):
    db.execute(remove_all_invite_friend_query, (useruid, useruid))

# -- ����Ʈ ����
def get_questlist_db(db, useruid, status, quest_subtype=None):
# -- ���ǿ� �´� ���� ��������
    if quest_subtype != None:
        tempq = quest_list_info_query.format(quest_status_list=",".join(map(str, status)))
        rs = db.query(tempq, (useruid, quest_subtype, ))
    else:
        rs = db.query(quest_reward_object_query, (useruid, status,))
    return rs if len(rs) !=0 else None

# -- useruid �� questid �� ���� ��������
def get_quest_db(db, useruid, quest_id):
    rs = db.query(quest_info_query, (useruid, quest_id,))
    if not rs:
        raise DBAccessError("get_quest_db error", useruid=useruid, quest_id=quest_id)

    return rs[0]

# -- ��ü ����Ʈ ���� �ҷ�����
def get_quest_all_db(db, useruid):
    rs = db.query(quest_all_info_query, (useruid,))
    #if not rs:
    #    raise DBAccessError("get_quest_all_db error", useruid=useruid) 
    return rs


# -- ����Ʈ ������Ʈ ( INSERT )
def modify_quest_db(db, useruid, quest):

    db.execute(modify_quest_query, (useruid, quest.quest_id, quest.quest_subtype, quest.count, quest.status, quest.count, quest.status,))
