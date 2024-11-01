
#include <iostream>

#include <io.h>
#include <stdio.h>
#include <stdlib.h>



void See_something(unsigned long long addr) {
	unsigned long long* address;
	address = (unsigned long long*)addr;
	printf("The content of the address : %p\n", *address);

};


char name[20];

char* getname(char* username) {
	return strdup(name);
}

int main() {
	printf("Main:%p\n", &main);
	setvbuf(stdout, 0, _IONBF, 0);
	char address[20];
	char message[256];
	unsigned long long addr = 0;
	puts("###############################");
	puts("Do you know return to library ?");
	puts("###############################");
	printf("Name:");
	read(0, name, 20);
	puts("What do you want to see in memory?");
	printf("Give me an address (in hex) :");
	read(0, address, 20);
	addr = strtoll(address, 0, 16);
	See_something(addr);
	printf("Leave some message for me :");
	read(0, message, 0x400);
	printf("%s\n", message);
	puts("Thanks you");
	getname(name);
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
