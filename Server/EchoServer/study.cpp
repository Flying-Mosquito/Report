#include "Client_info.h"
#include "Protocol.h"
#include"Sector.h"
#include<iostream>
#include<vector>
#include<thread>
using namespace std;

HANDLE io;	//빈 포트 생성
int ID = 0;
Client_info Player[8];
View ViewList[10][10];

void AcceptThread();
void WorkerThread();
void LobbyThread();
void ProcessPacket(int id,char* ptr);
void Send_Packet(int client, void* packet);

int main()
{
	srand((unsigned)time(NULL));
	WSADATA wsa;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
		cout << "초기화 error" << endl;

	//섹터 범위 셋팅
	for (int i = 0; i < 10; ++i)
	{
		for (int j = 0; j < 10; ++j)
		{
			ViewList[i][j].x = (800 / 10)*j;
			ViewList[i][j].y = (600 / 10)*i;
		}
	}

	SYSTEM_INFO is;
	GetSystemInfo(&is);

	vector<thread*> Worker;

	io = CreateIoCompletionPort(INVALID_HANDLE_VALUE, NULL, NULL, 0);

	for (auto i = 0; i < (int)is.dwNumberOfProcessors; ++i)
	{
		Worker.push_back(new thread{ WorkerThread });
	}

	auto Acceptex = thread{ AcceptThread };
	auto Lobby = thread{ LobbyThread };

	while (1)
	{
		Sleep(1000);
	}

	Acceptex.join();
	Lobby.join();

	for (auto t : Worker)
	{
		t->join();
	}
}

void AcceptThread()
{
	cout << "시작" << endl;

	SOCKET listen_sock;
	SOCKADDR_IN  addr;

	listen_sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP,
		NULL, 0, WSA_FLAG_OVERLAPPED);

	//주소 설정
	ZeroMemory(&addr, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(INADDR_ANY);
	addr.sin_port = htons(9000);

	//bind 부분
	int retval = 0;
	retval = ::bind(listen_sock, (SOCKADDR*)&addr, sizeof(addr));
	if (retval == SOCKET_ERROR)
		cout << "Bind Error" << endl;

	//리슨 소켓 설정
	retval = listen(listen_sock, SOMAXCONN);
	if (retval == INVALID_SOCKET)
	{
		cout << "listen_sock error" << endl;
	}

	SOCKET client_sock;
	SOCKADDR_IN client_addr;

	client_sock = NULL;

	while (1)
	{
		int len = sizeof(client_addr);
		client_sock = WSAAccept(listen_sock, (SOCKADDR*)&client_addr,
			&len, NULL, NULL);

		if (client_sock == INVALID_SOCKET)
			cout << "클라이언트 소켓 에러" << endl;

		Player[ID].over_ex.s = client_sock;

		CreateIoCompletionPort((HANDLE)client_sock, io, ID, 0);
		cout << ID << " 접속완료" << endl;

		//Player[ID].over_ex.buf.buf = Player[ID].over_ex.Packetbuf;
		//Player[ID].over_ex.buf.len = sizeof(Player[ID].over_ex.Packetbuf);

		unsigned long recvflag = 0;
		WSARecv(client_sock, &Player[ID].over_ex.buf,
			1, NULL, &recvflag,
			(LPOVERLAPPED)&Player[ID].over_ex.Overlapped, NULL);
		//클라이언트별 개별 아이디 부여
		ID++;
	}
}

void LobbyThread()
{
	//while (1)
	//{
	//	cout << "ㅣㅠㅣㅠㅣㅣㅠ니인ㅁ임닝" << endl;
	//}
}

void WorkerThread()
{
	//패킷 재조립이란?
	int retval;
	unsigned long iosize;
	unsigned long Object_ID;
	unsigned long ioflag = 0;
	Over_ex *Over = nullptr;
	while (1)
	{
		GetQueuedCompletionStatus(io, &iosize, &Object_ID,
			reinterpret_cast<LPOVERLAPPED *>(&Over), INFINITE);

		if (iosize == 0)
		{
			//cout << iosize << endl;
			closesocket(Over->s);
			//WSAGetOverlappedResult
			//게임종료 처리
		}

		if (Over->operationtype == Recvtype)
		{
			//cout << iosize << endl;
			//cout << "Recvtype" << endl;
			char *Buf = Over->iocpbuf;	//?
			unsigned long data_to_process = iosize;
			Over->currentsize = data_to_process;

			while (data_to_process > 0)
			{
				if (Over->currentsize == 0)
					Over->currentsize = Buf[0];

				unsigned int need_to_build =
					Over->currentsize - Over->prevsize;

				if (data_to_process >= need_to_build)
				{
					//조립
					memcpy(Over->Packetbuf + Over->prevsize, Buf, need_to_build);
					//cout << static_cast<int>(Object_ID) << endl;
					ProcessPacket(static_cast<int>(Object_ID), Over->Packetbuf);

					Over->currentsize = 0;
					Over->prevsize = 0;
					Buf += need_to_build;
					data_to_process -= need_to_build;
				}
				else
				{
					//훗날을 기약해
					memcpy(Over->Packetbuf + Over->prevsize, Buf, data_to_process);
					Over->prevsize += data_to_process;
					data_to_process = 0;
				}

			}
			retval = WSARecv(Over->s, &Over->buf, 1, NULL, &ioflag, &Over->Overlapped, NULL);
		}

		else if (Over->operationtype == Sendtype)
		{
			delete Over;
		}
	}
}

void ProcessPacket(int id,char *ptr)
{
	//cout << "processpacket 진입" << endl;
	//cout <<"id : "<< id << endl;
	switch (ptr[1])
	{
	case CS_LOGIN:
	{
		cout << "로그인 요청" << endl;
		cout << "id : " << id << endl;

		Player[id].setPlayerID(id);
		Player[id].setPlayerUse(true);

		sc_packet_putplayer login;
		login.size = sizeof(sc_packet_putplayer);
		login.id = Player[id].getPlayerID();
		//cout << login.id <<endl;
		login.type = SC_LOGIN;
		Send_Packet(id, &login);
 
		break;
	}
	case CS_LEFT:
		Player[id].setPlayerPosX(Player[id].getPlayerPosX() - 1);
		//cout << "L" << endl;
		//cout << "pid:" << packet->id<<"px: "<<packet->x << "ptype:" << packet->type << endl;
		break;	
	case CS_RIGHT:
		Player[id].setPlayerPosX(Player[id].getPlayerPosX() + 1);
		break;
	case CS_UP:
		Player[id].setPlayerPosY(Player[id].getPlayerPosY() - 1);
		break;
	case CS_DOWN:
		Player[id].setPlayerPosY(Player[id].getPlayerPosY() + 1);
		break;

	default:
		break;
	}

	//매번 플레이어들의 위치값 갱신
	
	sc_packet_move packet;
	packet.size = sizeof(sc_packet_move);
	packet.id = Player[id].getPlayerID();
	packet.type = SC_POS;
	packet.x = Player[id].getPlayerPosX();
	packet.y = Player[id].getPlayerPosY();
	packet.Sectorx = Player[id].getPlayerPosX() / 80;
	packet.Sectory = Player[id].getPlayerPosY() / 60;
	/*cout << ViewList[Player[id].getPlayerPosX() / 80][Player[id].getPlayerPosY() / 60].x <<
		ViewList[Player[id].getPlayerPosX() / 60][Player[id].getPlayerPosY() / 80].y << endl;*/

	for (int p = 0; p < 8; ++p)
	{
		if (Player[p].getPlayerUse() == true)
		{
			cout << Player[p].getPlayerPosX() / 80 << "," << Player[p].getPlayerPosY() / 60 << endl;
			Send_Packet(p, &packet);
			cout << "id : " << Player[p].getPlayerID()
				<< "x : " << Player[p].getPlayerPosX()
				<< "y : " << Player[p].getPlayerPosY() << endl;

		}
		//cout << Player[i].getPlayerUse() << endl;
	}
}

void Send_Packet(int client, void* packet)
{
//	char* a = reinterpret_cast<char*>(packet);
	int packet_size = reinterpret_cast<unsigned char*>(packet)[0];
	Over_ex *Send_Operation = new Over_ex;
	ZeroMemory(Send_Operation, sizeof(Over_ex));

	Send_Operation->operationtype = Sendtype;

	Send_Operation->buf.buf = Send_Operation->Packetbuf;
	Send_Operation->buf.len = packet_size;

//	sc_packet_move *b = reinterpret_cast<sc_packet_move*>(packet);
//	char *c = reinterpret_cast<char*>(packet);

	memcpy(Send_Operation->Packetbuf, reinterpret_cast<char*>(packet), packet_size);
	
//	sc_packet_move *p = reinterpret_cast<sc_packet_move*>(Send_Operation->Packetbuf);
//	cout << "id:" << p->id<<"x :"<<p->x << "type:" << static_cast<char>(p->type) << endl;

	DWORD iobyte;
	int retval;
	retval=WSASend(Player[client].over_ex.s, &Send_Operation->buf, 1,
		&iobyte, 0, &Send_Operation->Overlapped, NULL);
	if (retval != 0)
		cout << "error sendpacket" << endl;
	cout <<client<< "정보 Send" << endl;


}
