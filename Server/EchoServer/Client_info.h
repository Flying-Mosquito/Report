#pragma once
#include <Winsock2.h>
#include <time.h>

enum{
	Sendtype = 1,
	Recvtype = 2
};

struct Over_ex	//오버렙트구조체 확장
{
	OVERLAPPED Overlapped;
	SOCKET s;
	int operationtype;	//패킷의 타입
	int prevsize;	//이전데이타 크기
	int currentsize;//현재데이타 크기
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

