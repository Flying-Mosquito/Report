# -*- coding: utf-8 -*-
# ------ 쿼리

# --- 중복체크 처리 쿼리
check_duplicate_username_query = "select username from users where username=%s"
check_duplicate_nickname_query = "select nickname from users where nickname=%s"

# --- 랭킹 등록 점수들 가져오기
get_rank_score_all_query = "select rank_score from ranking"

# --- 초기화 쿼리
init_account_query = "insert into users values(NULL,%s,%s,%s,1,0,100,0)"
init_skill_query = "insert into skills values(%s,1,100,1,100,1,100)"
init_ranking_query = "insert into ranking values(%s,%s,%s)"
init_item_query = "insert into item values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

# --- 상태 변경 (점수 더하는 경우)
user_update_level_query = "update users set level=level+%s where useruid=%s"
user_update_exp_query = "update users set exp=exp+%s where useruid=%s"
user_update_money_query = "update users set money=money+%s where useruid=%s"
user_update_score_query = "update users set score=score+%s where useruid=%s"

update_skill_level_query = "update skills set skill_level=skill_level+%s where skill_useruid=%s"
update_skill_level2_query = "update skills set skill_level2=skill_level2+%s where skill_useruid=%s"
update_skill_level3_query = "update skills set skill_level3=skill_level3+%s where skill_useruid=%s"
update_skill_cost_query = "update skills set skill_cost=skill_level+%s where skill_useruid=%s"
update_skill_cost2_query = "update skills set skill_cost2=skill_cost2+%s where skill_useruid=%s"
update_skill_cost3_query = "update skills set skill_cost3=skill_cost3+%s where skill_useruid=%s"

update_item_num_query = "update item set item_num=item_num+%s where item_useruid=%s"
update_item_num2_query = "update item set item_num2=item_num2+%s where item_useruid=%s"
update_item_num3_query = "update item set item_num3=item_num3+%s where item_useruid=%s"

# --- 상태 수정 (값을 아예 바꾸고 싶을 때)
modify_level_query = "update users set level=%s where useruid=%s"
modify_exp_query = "update users set exp=%s where useruid=%s"
modify_money_query = "update users set money=%s where useruid=%s"
modify_score_query = "update users set score=%s where useruid=%s"

modify_skill_level_query = "update skills set skill_level=%s where skill_useruid=%s"
modify_skill_level2_query = "update skills set skill_level2=%s where skill_useruid=%s"
modify_skill_level3_query = "update skills set skill_level3=%s where skill_useruid=%s"
modify_skill_cost_query = "update skills set skill_cost=%s where skill_useruid=%s"
modify_skill_cost2_query = "update skills set skill_cost2=%s where skill_useruid=%s"
modify_skill_cost3_query = "update skills set skill_cost3=%s where skill_useruid=%s"

modify_item_num_query = "update item set item_num=%s where item_useruid=%s"
modify_item_num2_query = "update item set item_num2=%s where item_useruid=%s"
modify_item_num3_query = "update item set item_num3=%s where item_useruid=%s"
modify_item_id_query = "update item set item_id=%s where item_useruid=%s"
modify_item_id2_query = "update item set item_id2=%s where item_useruid=%s"
modify_item_id3_query = "update item set item_id3=%s where item_useruid=%s"
modify_item_type_query = "update item set item_type=%s where item_useruid=%s"
modify_item_type2_query = "update item set item_type2=%s where item_useruid=%s"
modify_item_type3_query = "update item set item_type3=%s where item_useruid=%s"

# --- 불러오기 쿼리
get_passwd_query = "select password from users where username=%s"
get_useruid_query = "select useruid from users where username=%s"
get_level_query = "select level from users where useruid=%s"
get_exp_query = "select exp from users where useruid=%s"
get_money_query = "select money from users where useruid=%s"
get_score_query = "select score from users where useruid=%s"

get_skill_level_query = "select skill_level,skill_level2,skill_level3 from skills where skill_useruid=%s"
get_skill_cost_query = "select skill_cost,skill_cost2,skill_cost3 from skills where skill_useruid=%s"

get_ranking_query = "select ranking from ranking where useruid=%s"

get_item_num_query = "select item_num,item_num2,item_num3 from item where item_useruid=%s"
get_item_type_query = "select item_type,item_type2,item_type3 from item where item_useruid=%s"
get_item_id_query = "select item_id,item_id2,item_id3 from item where item_useruid=%s"

# --- 쿼리 끝
