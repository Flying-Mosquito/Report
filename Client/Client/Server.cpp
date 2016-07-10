#include "Server.h"

Server::Server()
{

}
Server::~Server()
{

}
void Server::setSocket_HWND(HWND s){
	Socket_HWND = s;
}
void Server::setHINSTANCE(HINSTANCE g)
{
	g_hInst = g;
}
int Server::socketinit()
{
	for (int i = 0; i < 10; ++i)
	{
		for (int j = 0; j < 10; ++j)
		{
			ViewList[i][j].x = (800 / 10)*j;
			ViewList[i][j].y = (600 / 10)*i;
		}
	}

	WSADATA wsa;
	int ret = 0;

	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
		cout << "winsock init error" << endl;

	sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, NULL, 0);

	SOCKADDR_IN addr;

	ZeroMemory(&addr, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = inet_addr("127.0.0.1");
	addr.sin_port = htons(9000);

	ret = WSAConnect(sock, (SOCKADDR*)&addr, sizeof(addr), NULL, NULL, NULL, NULL);

	WSAAsyncSelect(sock, Socket_HWND, WM_SOCKET, FD_READ | FD_CLOSE);

	WSA_send_buf.buf = Send_buf;
	WSA_send_buf.len = MAX_SIZE;
	WSA_recv_buf.buf = Recv_buf;
	WSA_recv_buf.len = MAX_SIZE;

	DWORD iobyte;

	cs_packet_accept *login =
		reinterpret_cast<cs_packet_accept*>(Send_buf);
	login->size = sizeof(cs_packet_accept);
	login->type = CS_LOGIN;

	ret = WSASend(sock, &WSA_send_buf, 1, &iobyte, 0, NULL, NULL);
	//cout << iobyte << endl;
	if (ret == SOCKET_ERROR)
		cout << "WSASend Error" << endl;

	return 1;
}
void Server::KeyDown(WPARAM wParam)
{
	int x = 0, y = 0, retval = 0;
	DWORD iobyte;
	DWORD ioflag = 0;

	if (wParam == VK_UP) y += 1;
	if (wParam == VK_DOWN) y -= 1;
	if (wParam == VK_LEFT) x -= 1;
	if (wParam == VK_RIGHT) x += 1;

	cs_packet_move *my_packet = reinterpret_cast<cs_packet_move*>(Send_buf);
	my_packet->size = sizeof(my_packet);
	WSA_send_buf.len = sizeof(my_packet);
	if (0 != x)
	{
		if (x == 1)
		{
			my_packet->type = CS_RIGHT;
		}
		else
		{
			my_packet->type = CS_LEFT;
		}
		retval = WSASend(sock, &WSA_send_buf, 1, &iobyte, ioflag, NULL, NULL);
		//cout << iobyte << endl;
		if (retval == SOCKET_ERROR)
		{
			cout << "WSASend() x Error" << endl;
			cout << WSAGetLastError() << endl;
		}
	}
	if (0 != y)
	{
		if (y == 1)
		{
			my_packet->type = CS_UP;
		}
		else
		{
			my_packet->type = CS_DOWN;
		}
		retval = WSASend(sock, &WSA_send_buf, 1, &iobyte, ioflag, NULL, NULL);
		if (retval == SOCKET_ERROR)
		{
			cout << "WSASend() x Error" << endl;
			cout << WSAGetLastError() << endl;
		}
	}
}
void Server::ReadPacket()
{
	DWORD iobyte, ioflag = 0;

	int ret = WSARecv(sock, &WSA_recv_buf, 1, &iobyte, &ioflag, NULL, NULL);
	if (ret != 0)
	{
		int err_code = WSAGetLastError();
		cout << "Recv Error : " << err_code << endl;
	}
	cout << "recv" << endl;
	BYTE *ptr = reinterpret_cast<BYTE*>(Recv_buf);

	while (0 != iobyte)
	{
		if (in_packet_size == 0)
		{
			in_packet_size = ptr[0];
		}

		if (iobyte + save_packet_size >= in_packet_size)
		{
			memcpy(Complete_buf + save_packet_size,
				ptr,
				in_packet_size - save_packet_size);

			ProcessPacket(Complete_buf);

			ptr += in_packet_size - save_packet_size;
			iobyte -= in_packet_size - save_packet_size;
			in_packet_size = 0;
			save_packet_size = 0;
		}
		else
		{
			memcpy(Complete_buf + save_packet_size, ptr, iobyte);
			save_packet_size += iobyte;
			iobyte = 0;
		}

	}
}
//int Server::getPlayerID()
//{
//	return P_id;
//}
//int Server::getPlayerPosX()
//{
//	return P_x;
//}
//int Server::getPlayerPosY()
//{
//	return P_y;
//}
//void Server::setPlayerPosX(int x)
//{
//	P_x = x;
//}
//void Server::setPlayerPosY(int y)
//{
//	P_y = y;
//}
//void Server::setPlayerID(int id)
//{
//	P_id = id;
//}


void Server::ProcessPacket(char* ptr)
{
	//cout << "process" << endl;
	switch (ptr[1])
	{

	case SC_LOGIN:
	{
		sc_packet_putplayer *p =
			reinterpret_cast<sc_packet_putplayer*>(ptr);
		my_id = p->id;
		//Player[my_id].P_id = my_id;
		cout << "my_id : "<< my_id << endl;
		break;
	}

	case SC_POS:
	{
		cout << "pos" << endl;
		sc_packet_move *p =
			reinterpret_cast<sc_packet_move*>(ptr);
		//cout << p->id << "," << p->x << "," << p->y << endl;
		cout << p->Sectorx << "," << p->Sectory << endl;
		cout << ViewList[p->Sectorx][p->Sectory].x<< ViewList[p->Sectorx][p->Sectory].y << endl;
		if (p->id == my_id)
		{
			Player[my_id].P_x = p->x;
			Player[my_id].P_y = p->y;
			Player[my_id].P_Sectorx = p->Sectorx;
			Player[my_id].P_Sectory = p->Sectory;
		}

		else
		{
			Player[p->id].P_x = p->x;
			Player[p->id].P_y = p->y;
			Player[p->id].P_Sectorx = p->Sectorx;
			Player[p->id].P_Sectory = p->Sectory;

			cout << Player[p->id].P_id
				<< "," << Player[p->id].P_x
				<< ","
				<< Player[p->id].P_y << endl;
		}
		break;
	}

	}
}

void Server::SendPacket(SOCKET s, void* buf)
{
	SOCKET Send_socket = s;
	int packet_size = reinterpret_cast<char*>(buf)[0];
	memcpy(Complete_buf, buf, packet_size);

	WSA_Complete_buf.buf = Complete_buf;
	WSA_Complete_buf.len = packet_size;
	DWORD iobyte;
	WSASend(Send_socket, &WSA_Complete_buf, 1, &iobyte, 0, NULL, NULL);
}

//void Send_Packet(SOCKET temp, void *packet)
//{
//   SOCKET g_mysocket = temp;
//   int packet_size = reinterpret_cast<char *>(packet)[0];
//   memcpy(Complete_buffer, packet, packet_size);
//
//   temp_wsabuf.buf = Complete_buffer;
//   temp_wsabuf.len = packet_size;
//   DWORD iobyte;
//   WSASend(g_mysocket, &temp_wsabuf,
//      1, &iobyte, 0, NULL, NULL);
//}

int Server::GetMy_id()
{
	return my_id;
}