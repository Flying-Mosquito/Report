
SQL_UP = """
-- 유저 테이블
create table user (

	useruid	bigint	not null	AUTO_INCREMENT,	-- 고유 번호
	username	varchar(10)	not null,	-- 아이디
	password	varchar(10)	not null,	-- 비밀번호
	nickname	varchar(10)	not null,	-- 닉네임

	level	bigint	not null,			-- 레벨
	exp	bigint	not null,			-- 경험치
	money	bigint	not null,			-- 재화
	score	bigint	not null,			-- 랭킹 점수

	primary key (useruid)
) engine = InnoDB default charset=utf8;

create table item (
	
	useruid	bigint	not null,	-- 유저 고유번호
	itemuid	bigint not null	AUTO_INCREMENT,	-- 아이템 고유번호
	item_id	varchar(30)	not null,	-- 아이템 이름
	item_type	varchar(10)	not null,	-- 아이템 타입(장착식, 소모식)
	item_num	bigint	not null,	-- 아이템 소지 개수
	slot	tinyint	not null,		-- 장착부위

	primary key(useruid, itemuid)
) engine = InnoDB default charset=utf8;

create table skill (

	useruid bigint	not null,	-- 유저 고유 번호
	skilluid	bigint	not null	AUTO_INCREMENT,	-- 스킬 고유 번호
	skillid	varchar(30)	not null,	-- 스킬 이름
	skill_level	tinyint	not null,	-- 스킬 레벨
	skill_cost	tinyint not null,	-- 코스트

	primary key(useruid, skilluid)
) engine = InnoDB default charset=utf8;

create table ranking (

	useruid bigint	not null,	-- 유저 고유번호
	rank_score	bigint	not null,	-- 랭킹 점수
	ranking	bigint	not null,	-- 랭킹

	primary key(useruid, ranking)
) engine = InnoDB default charset=utf8;

create table invite_friend (
	invite_useruid	bigint	not null,
	accept_useruid	bigint	not null,
	ctime	timestamp	not null default current_timestamp,
	status	enum('R','A','D','E')	not null, -- 상태( R : 친구신청, A : 수락, D : 거절, E : 삭제)
	
	primary key(invite_useruid, accept_useruid)
) engine = InnoDB default charset=utf8;

create table user_stage (
	useruid	bigint not null,
	stage_id	int	not null,
	stage_uid	int	not null,
	exp_potion	int	not null default 0,	-- 0: 미사용 1: 사용
	start_date	timestamp	not null default current_timestamp, -- 게임 시작
	access		int	not null default 0,	-- 미입장, 입장
	clear_date	timestamp	not null,	-- 클리어 시간
	clear_sum	int	not null,		-- 클리어 횟수
	reward_count	int	not null default 0,	-- 보상
	add_reward_count	int	not null default 0, -- 추가 보상
	primary key(useruid, stage_id)
) engine = InnoDB default charset=utf8;

create table user_quest (
	useruid             bigint      not null,
	quest_id            int         not null,
	quest_subtype       int         not null,
	count               int         not null,
	status              int         not null,
	primary key(useruid, quest_id)
) engine = InnoDB default charset=utf8;

SQL_DOWN = """
drop table user;
drop table item;
drop table skill;
drop table ranking;
drop table invite_friend;
drop table user_stage;
drop table user_quest;
"""

step(SQL_UP, SQL_DOWN)
