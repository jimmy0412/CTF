// Winmagic.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <iostream>
#include <io.h>
#define _CRT_RAND_S  
#include <stdlib.h>
#include <time.h>
#include <windows.h>

void get_flag2() {
	
	char key[] = "Do_you_know_why_my_teammate_Orange_is_so_angry?????";
	char cipher[] = {}
	for (int i = 0; i < sizeof(cipher); i++) {
		printf("%c", cipher[i] ^ key[i]);
	}
	getchar();
}



void get_flag3() {
	char key[] = "Do_you_know_why_my_teammate_jeffxx_is_so_angry??????????";
	char cipher[] = {}
	for (int i = 0; i < sizeof(cipher); i++) {
		printf("%c", cipher[i] ^ key[i] ^ rand());
	}
	getchar();
}

void get_flag() {
	int password;
	int magic;
	HANDLE hstdin;
	srand(time(NULL));
	char key[] = "Do_you_know_why_my_teammate_ddaa_is_so_angry??????";
	char cipher[] = {}
	password = rand();

	printf("Give me maigc :");

	scanf_s("%d", &magic);
	if (password == magic) {
		for (int i = 0; i < sizeof(cipher); i++) {
			printf("%c", cipher[i] ^ key[i]);
		}
	}
	getchar();

};


int main()
{
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	get_flag();
	if ((int)&main == 0xddaa) {
		get_flag2();
		get_flag3();
	}
}
