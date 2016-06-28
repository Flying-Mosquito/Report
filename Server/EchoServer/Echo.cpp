#include<winsock2.h>
#include<iostream>
#include<thread>
#include<vector>
#define BUFSIZE 512
using namespace std;

void inputthread();
void outputthread();
void acceptthread();
void err_display(char *msg, int err_no)
{
	WCHAR *lpMsgBuf;
	FormatMessage(
		FORMAT_MESSAGE_ALLOCATE_BUFFER |
		FORMAT_MESSAGE_FROM_SYSTEM,
		NULL, err_no,
		MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
		(LPTSTR)&lpMsgBuf, 0, NULL);
	printf("%s", msg);
	wprintf(L"에러[%s]\n", lpMsgBuf);
	LocalFree(lpMsgBuf);
}

char buf[BUFSIZE];
vector<SOCKET> v;
SOCKET client_sock;
SOCKADDR_IN client_addr;

int main()
{
	//윈속 초기화
	WSADATA wsa;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
		return false;
	
	auto acceptx = thread{ acceptthread };
	auto input = thread{ inputthread };
	auto ouput = thread{ outputthread };
	while (1)
	{
		Sleep(1000);
	}
	acceptx.join();	//알아보기
	input.join();
	ouput.join();

	WSACleanup();

}

void acceptthread()
{
	SOCKET listen_sock;
	SOCKADDR_IN  addr;

	listen_sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP,
		NULL, 0, WSA_FLAG_OVERLAPPED);

	//주소 설정
	ZeroMemory(&addr, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.S_un.S_addr = htonl(INADDR_ANY);
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

	while (1)
	{
		int len = sizeof(client_addr);
		client_sock = WSAAccept(listen_sock, (SOCKADDR*)&client_addr,
			&len, NULL, NULL);
		if (client_sock == INVALID_SOCKET)
			cout << "WSAAccept Error" << endl;
		cout << inet_ntoa(client_addr.sin_addr) << 
			ntohs(client_addr.sin_port) << endl;
		v.push_back(client_sock);
	}

	client_sock = NULL;
	ZeroMemory(&client_addr, sizeof(client_addr));
}

void inputthread()
{
	int retval = 0;
	for (auto temp : v)
	{
		retval = send(v[temp], buf, sizeof(buf), 0);
		if (retval == 0)
		{
			cout << "send error" << endl;
		}
		for (int i = 0; i < BUFSIZE;++i)
			cout << buf[i];
	}
}
void outputthread()
{
	int retval = 0;
	while (1)
	{
		cout << "?"<<retval;
		retval = recv(client_sock, buf, sizeof(buf), 0);
		if (retval == 0)
		{
			cout << "recv error" << endl;
		}
		for (int i = 0; i < BUFSIZE; ++i)
		{
			if (buf[i] == NULL)
				break;
			cout << buf[i];
		}
		//cout << endl;
	}
}



//#include <chrono>
//#include <iostream>
//#include<stdio.h>
//#include <windows.h>
//#include <mutex>
//#include <thread>
//#include <vector>
//
//using namespace std;
//using namespace std::chrono;
//
//mutex mylock;
//volatile int sum = 0;
//
//vector<thread*> v;
//
//void thread_func(int num_threads)
//{
//	volatile int local_sum = 0;
//	for (auto i = 1; i <= 50000000 / num_threads; i++)
//		local_sum += 2;
//	
//	mylock.lock();
//	sum += local_sum;
//	mylock.unlock();
//}
//
//int main()
//{
//	for (auto i = 1; i <= 4; i *= 2)
//	{
//		sum = 0;
//		v.clear();
//		auto t = high_resolution_clock::now();
//
//		for (auto j = 0; j<i; ++j) 
//			v.push_back(new thread(thread_func, i));
//
//		for (auto temp : v){
//			temp->join();
//		}
//		auto d = high_resolution_clock::now() - t;
//		cout << "Sum = " << sum << "\n";
//		cout << duration_cast<milliseconds>(d).count() << "msecs\n";
//	}
//}