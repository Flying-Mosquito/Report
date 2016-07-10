#pragma once
class Player
{
	int P_x;
	int P_y;
	int P_id;
	bool Play;

public:
	Player();
	~Player();

	bool getPlay();
	int getPlayerPosX();
	int getPlayerPosY();
	int getPlayerID();

	void setPlay(bool p);
	void setPlayerID(int id);
	void setPlayerPosX(int x);
	void setPlayerPosY(int y);
};

