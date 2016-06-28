#pragma once
#include <Winsock2.h>
#include <time.h>

enum{
	Sendtype = 1,
	Recvtype = 2
};

struct Over_ex	//������Ʈ����ü Ȯ��
{
	OVERLAPPED Overlapped;
	SOCKET s;
	int operationtype;	//��Ŷ�� Ÿ��
	int prevsize;	//��������Ÿ ũ��
	int currentsize;//���絥��Ÿ ũ��
	WSABUF buf;
	char Packetbuf[255];
	char iocpbuf[4000];
};

class Client_info
{
	int My_x;
	int My_y;
	int My_id;
	bool Use;
public:
	Over_ex over_ex;

	bool getPlayerUse();

	int getPlayerPosX();
	int getPlayerPosY();
	int getPlayerID();

	void setPlayerUse(bool u);

	void setPlayerPosX(int x);
	void setPlayerPosY(int y);
	void setPlayerID(int id);

	Client_info();
	~Client_info();
};

