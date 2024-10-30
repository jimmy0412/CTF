#include<stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include<assert.h>
int main(){

    int fd ;
    char ans[] = "sasqtxxbfgctceji";
    char buffer[] = "0";
    fd = open("/proc/pwncollege",2);
    assert(fd >0);
    write(fd,ans,sizeof(ans));
    //read(fd,buffer,100);
    //printf("%s",buffer);

    return 0 ;
}