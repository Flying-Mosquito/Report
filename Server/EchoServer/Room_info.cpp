#include "Room_info.h"

Room_info::Room_info()
{
	Max_User = false;
	Game_starting = false;
	Use_Room = false;
	ID.reserve(8);
}
Room_info::~Room_info()
{

}
bool Room_info::Check_Full_Room()
{
	int i = 0;
	for (auto t : ID)
	{
		if (ID[i] != NULL)
		{
			++i;
			if (i == 8)
			{
				Max_User = true;
				break;
			}
		}
	}
	return 0;
}
void Room_info::setMax_User(bool ft)
{
	Max_User = ft;
}
void Room_info::setGame_starting(bool ft)
{
	Game_starting = ft;
}
void Room_info::setUse_Room(bool ft)
{
	Use_Room = ft;
}
void Room_info::Push_ID(int id)
{
	ID.push_back(id);
}
void Room_info::setRoom_Num(int num)
{
	Room_Num = num;
}