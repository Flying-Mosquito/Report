#pragma once

#include<vector>

class Room_info
{
	int Room_Num;
	std::vector<int> ID;
	bool Max_User;
	bool Game_starting;
	bool Use_Room;
public:
	//static Room_info *getinstangce()
	//{
	//	static Room_info inst;
	//	return &inst;
	//}
	Room_info();
	~Room_info();
	bool Check_Full_Room();
	void setMax_User(bool ft);
	void setGame_starting(bool ft);
	void setUse_Room(bool ft);
	void Push_ID(int id);
	void setRoom_Num(int num);
};

