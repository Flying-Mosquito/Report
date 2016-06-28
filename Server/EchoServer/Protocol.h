#include <Windows.h>

#define WM_SOCKET WM_USER+1
#define MAX_SIZE 1024

#define SC_POS 1
#define SC_LOGIN 2

#define CS_LEFT 1
#define CS_RIGHT 2
#define CS_UP 3
#define CS_DOWN 4
#define CS_LOGIN 5

#pragma pack (push, 1)
//���� -> Ŭ��
struct sc_packet_move
{
	BYTE size;
	BYTE type;
	int id;
	int x;
	int y;
	int Sectorx;
	int Sectory;
};

struct sc_packet_putplayer
{
	BYTE size;
	BYTE type;
	int id;
};


//Ŭ�� -> ����
struct cs_packet_move
{
	BYTE size;
	BYTE type;
};

struct cs_packet_accept
{
	BYTE size;
	BYTE type;
};

#pragma pack (pop)