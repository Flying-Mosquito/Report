#include "Client_info.h"


Client_info::Client_info()
{
	My_x = (rand() % 60) * 10;
	My_y = (rand() % 60) * 10;
	My_id = -1;
	Use = false;

	over_ex.s = NULL;
	over_ex.operationtype = Recvtype;
	over_ex.prevsize = 0;
	over_ex.currentsize = 0;
	over_ex.buf.buf = over_ex.iocpbuf;
	over_ex.buf.len = sizeof(over_ex.iocpbuf);
	ZeroMemory(&over_ex.Overlapped, sizeof(over_ex.Overlapped));
}

Client_info::~Client_info()
{

}

bool Client_info::getPlayerUse()
{
	return Use;
}

int Client_info::getPlayerPosX()
{
	return My_x;
}

int Client_info::getPlayerPosY()
{
	return My_y;
}
int Client_info::getPlayerID()
{
	return My_id;
}


void Client_info::setPlayerUse(bool use)
{
	Use = use;
}

void Client_info::setPlayerPosX(int x)
{
	My_x = x;
}
void Client_info::setPlayerPosY(int y)
{
	My_y = y;
}

void Client_info::setPlayerID(int id)
{
	My_id = id;
}