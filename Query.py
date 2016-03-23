# -*- coding: utf-8 -*-

# ----- 쿼리 모음
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

# ------ /쿼리 모음

# 게임에 가입 된 유저인지 확인
def get_useruid_nickname_db(db, useruid, nickname):
    account_rs = db.query(get_useruid_nickname_query, (useruid,))
    return account_rs

# 닉네임 중복 체크
def check_duplicate_nickname_db(db, nickname):
    nick_rs = db.query(check_duplicate_nickname_query, (nickname,))
    return nick_rs

# -- 유저의 친구들을 읽어온다.
def get_user_friend_list_db(db, useruid, status):
    rs = db.query(get_user_friend_list_query, (useruid, status))
    # 신규유저이거나 친구가 없는 유저라면 rs가 None이라도 오류가 아니다.
    return [x[0] for x in rs]

# -- 친구의 정보를 읽어온다.
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

# -- 가입된 유저인가 검사
def get_account_db(db, useruid):
    rs = db.query(get_account_query, (useruid,))
    if not rs:
        raise DBAccessError("get_account_db error, useruid could not be found", useruid=useruid)

# -- 유저 친구 리스트 MAX 확인
# -- 유저 친구 수락 대기 리스트 MAX 확인
# status = 10 -> 친구 리스트, status = 11 -> 수락 대기 리스트
def get_check_friend_list_db(db, useruid, status):
    rs = db.query(get_check_friend_list_query, (useruid, status))
    return rs[0][0]

# -- 유저 친구 상태 확인
# 서로 이미 친구 상태인지 확인
def get_check_already_db(db, useruid1, useruid2, status):
    rs = db.query(get_check_already_query,(useruid1, useruid2, status))
    return rs

# -- 유저 친구 수락 리스트 확인
# 이미 친구 신청 상태인지 확인
def get_check_friend_invite_db(db, invite_useruid, accept_useruid):
    rs = db.query(get_check_friend_invite_query, (invite_useruid, accept_useruid))
    return rs

# -- 유저 친구 수락 리스트 MAX 확인
def get_check_max_friend_invite_db(db, accept_useruid, status):
    rs = db.query(get_check_max_friend_invite_query, (accept_useruid, status))
    return rs[0][0]

# -- 친구 수락 대기 리스트 등록
def insert_invitefriend_list_db(db, invite_useruid, accept_useruid, status):
    db.execute(insert_invitefriend_list_query, (invite_useruid, accept_useruid, status))

# -- 친구 리스트 등록
def insert_friend_db(db, useruid1, useruid2, status):
    db.execute(insert_friend_query, (useruid1, useruid2, status, useruid2, useruid1, status , status))

# -- 친구 삭제 상태로 변경
def update_erase_friend_db(db, useruid1, useruid2, invite_status, erase_status):
    db.execute(update_friend_query, (erase_status, useruid1, useruid2, useruid2, useruid1, invite_status))

# -- 친구 수락 대기 리스트 삭제
def delete_invite_friend_db(db, invite_useruid, accept_useruid, status):
    db.execute(delete_invite_friend_query, (invite_useruid, accept_useruid, status))

# -- 친구 수락 대기 리스트 불러오기
def get_invite_friend_list_db(db, useruid, status):
    rs = db.query(get_invite_friend_list_query, (useruid, status))
    # 신규유저이거나 친구가 없는 유저라면 rs가 None이라도 오류가 아니다.
    return [x[0] for x in rs]

# -- 닉네임으로 검색
def get_userinfo_by_nickname_db(db, nickname):
    rs = db.query(get_userinfo_by_nickname_query, (u"{0}".format(nickname),))
    return rs

# -- 새 친구 요청 검색
def get_new_invite_friend_list_db(db, useruid, status, check_status):
    rs = db.query(get_new_invite_friend_list_query, (useruid, status, check_status))
    return [x[0] for x in rs]

# -- 친구 요청 new_check 상태를 0으로 업데이트
def update_new_check_invite_friend_db(db, useruid, check_status):
    db.execute(update_new_check_invite_friend_query, (check_status, useruid))

# -- 새 친구 검색
def get_new_friend_db(db, useruid, status, check_status):
    rs = db.query(get_new_friend_query, (useruid, status, check_status))
    return [x[0] for x in rs]

# -- 친구 new_check 상태 0으로 업데이트
def update_new_check_friend_db(db, useruid, check_status):
    db.execute(update_new_check_friend_query, (check_status, useruid))

# -- 탈퇴한 유저의 모든 친구 삭제
def remove_all_friend_db(db, useruid):
    db.execute(remove_all_friend_query, (useruid, useruid))

# -- 탈퇴한 유저의 수락대기리스트 삭제 및 탈퇴 유저가 신청한 친구 수락 요청 삭제
def remove_all_invite_friend_db(db, useruid):
    db.execute(remove_all_invite_friend_query, (useruid, useruid))

# -- 퀘스트 관련
def get_questlist_db(db, useruid, status, quest_subtype=None):
# -- 조건에 맞는 정보 가져오기
    if quest_subtype != None:
        tempq = quest_list_info_query.format(quest_status_list=",".join(map(str, status)))
        rs = db.query(tempq, (useruid, quest_subtype, ))
    else:
        rs = db.query(quest_reward_object_query, (useruid, status,))
    return rs if len(rs) !=0 else None

# -- useruid 와 questid 로 정보 꺼내오기
def get_quest_db(db, useruid, quest_id):
    rs = db.query(quest_info_query, (useruid, quest_id,))
    if not rs:
        raise DBAccessError("get_quest_db error", useruid=useruid, quest_id=quest_id)

    return rs[0]

# -- 전체 퀘스트 정보 불러오기
def get_quest_all_db(db, useruid):
    rs = db.query(quest_all_info_query, (useruid,))
    #if not rs:
    #    raise DBAccessError("get_quest_all_db error", useruid=useruid) 
    return rs


# -- 퀘스트 업데이트 ( INSERT )
def modify_quest_db(db, useruid, quest):

    db.execute(modify_quest_query, (useruid, quest.quest_id, quest.quest_subtype, quest.count, quest.status, quest.count, quest.status,))
