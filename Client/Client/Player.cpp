#include "Player.h"


Player::Player()
{
	P_x = -20;
	P_y = -20;
	P_id = -1;
	Play = false;
}


Player::~Player()
{
}

bool Player::getPlay()
{
	return Play;
}
int Player::getPlayerPosX()
{
	return P_x;
}
int Player::getPlayerPosY()
{
	return P_y;
}
int Player::getPlayerID()
{
	return P_id;
}

void Player::setPlay(bool p)
{
	Play = p;
}
void Player::setPlayerID(int id)
{
	P_id = id;
}
void Player::setPlayerPosX(int x)
{
	P_x = x;
}
void Player::setPlayerPosY(int y)
{
	P_y = y;
}