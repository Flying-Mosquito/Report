#pragma once
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#include<WinSock2.h>
#include<iostream>
#include<time.h>
#include"Protocol.h"

using namespace std;

#pragma pack(1)
struct Client_info
{
	int P_x;
	int P_y;
	int P_id;
	bool Play;
	int P_Sectorx;
	int P_Sectory;

	Client_info()
	{
		P_x = -20;
		P_y = -20;
		P_id = -1;
		Play = false;
	}
};
#pragma pack()

class Server
{
	HWND Socket_HWND;
	HINSTANCE g_hInst;

	//int P_x;
	//int P_y;
	//int P_id;

	SOCKET sock;
	WSABUF WSA_send_buf;
	char Send_buf[MAX_SIZE];
	WSABUF WSA_recv_buf;
	char Recv_buf[MAX_SIZE];
	WSABUF WSA_Complete_buf;
	char Complete_buf[MAX_SIZE];
	int in_packet_size;
	int save_packet_size;

	int my_id;
public:
	Client_info Player[8];
	View ViewList[10][10];

	LPCTSTR IpszClass = "Test Client";
//--------------------------------------------
	void setSocket_HWND(HWND s);
	void setHINSTANCE(HINSTANCE g);
//--------------------------------------
	static Server* getInstangce()
	{
		static Server inst;
		return &inst;
	}
//---------------------------------------
	Server();
	int socketinit(); 
	void ReadPacket();

	//int getPlayerPosX();
	//int getPlayerPosY();
	//int getPlayerID();

	//void setPlayerPosX(int x);
	//void setPlayerPosY(int y);
	//void setPlayerID(int id);

	void ProcessPacket(char* buf);
	void SendPacket(SOCKET s, void* buf);
	void KeyDown(WPARAM wParam);
	int GetMy_id();
	~Server();
};

