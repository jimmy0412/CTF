// play_with_win_sc.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "pch.h"
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <Windows.h>
#include <io.h>
int main() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	void *z = VirtualAlloc(NULL, 0x1000, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
	printf("Shellcode:");
	_read(0, z, 0x1000);
	// ((void(*)())sc)();
	void *x = z;
	((void(*)())x)();
	return 0;

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
