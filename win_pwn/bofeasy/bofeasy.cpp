// bofeasy.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <Windows.h>
#include <stdio.h>
#include <io.h>
#include <fcntl.h>


void l33t() {
	puts("Congrat !");
	WinExec("cmd.exe", 0);
}

int main()
{
	if ((rand() & 0xffff) == 0xddaa) {
		l33t();
	}
	char buf[0x30];
	setvbuf(stdout, 0, _IONBF, 0);
	printf("main: %p\n", &main);
	printf("Input:");
	_read(0, buf, 0x100);
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
