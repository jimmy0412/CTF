#include<stdio.h>
#include <fcntl.h>
int main(){
	int fd;
    fd = open("/tmp/456", O_WRONLY | O_APPEND | O_CREAT,0644);
}
