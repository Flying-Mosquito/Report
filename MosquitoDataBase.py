
SQL_UP = """
-- ���� ���̺�
create table user (

	useruid	bigint	not null	AUTO_INCREMENT,	-- ���� ��ȣ
	username	varchar(10)	not null,	-- ���̵�
	password	varchar(10)	not null,	-- ��й�ȣ
	nickname	varchar(10)	not null,	-- �г���

	level	bigint	not null,			-- ����
	exp	bigint	not null,			-- ����ġ
	money	bigint	not null,			-- ��ȭ
	score	bigint	not null,			-- ��ŷ ����

	primary key (useruid)
) engine = InnoDB default charset=utf8;

create table item (
	
	useruid	bigint	not null,	-- ���� ������ȣ
	itemuid	bigint not null	AUTO_INCREMENT,	-- ������ ������ȣ
	item_id	varchar(30)	not null,	-- ������ �̸�
	item_type	varchar(10)	not null,	-- ������ Ÿ��(������, �Ҹ��)
	item_num	bigint	not null,	-- ������ ���� ����
	slot	tinyint	not null,		-- ��������

	primary key(useruid, itemuid)
) engine = InnoDB default charset=utf8;

create table skill (

	useruid bigint	not null,	-- ���� ���� ��ȣ
	skilluid	bigint	not null	AUTO_INCREMENT,	-- ��ų ���� ��ȣ
	skillid	varchar(30)	not null,	-- ��ų �̸�
	skill_level	tinyint	not null,	-- ��ų ����
	skill_cost	tinyint not null,	-- �ڽ�Ʈ

	primary key(useruid, skilluid)
) engine = InnoDB default charset=utf8;

create table ranking (

	useruid bigint	not null,	-- ���� ������ȣ
	rank_score	bigint	not null,	-- ��ŷ ����
	ranking	bigint	not null,	-- ��ŷ

	primary key(useruid, ranking)
) engine = InnoDB default charset=utf8;

create table invite_friend (
	invite_useruid	bigint	not null,
	accept_useruid	bigint	not null,
	ctime	timestamp	not null default current_timestamp,
	status	enum('R','A','D','E')	not null, -- ����( R : ģ����û, A : ����, D : ����, E : ����)
	
	primary key(invite_useruid, accept_useruid)
) engine = InnoDB default charset=utf8;

create table user_stage (
	useruid	bigint not null,
	stage_id	int	not null,
	stage_uid	int	not null,
	exp_potion	int	not null default 0,	-- 0: �̻�� 1: ���
	start_date	timestamp	not null default current_timestamp, -- ���� ����
	access		int	not null default 0,	-- ������, ����
	clear_date	timestamp	not null,	-- Ŭ���� �ð�
	clear_sum	int	not null,		-- Ŭ���� Ƚ��
	reward_count	int	not null default 0,	-- ����
	add_reward_count	int	not null default 0, -- �߰� ����
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
