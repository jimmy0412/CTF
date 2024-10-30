from pwn import *

r = process('/home/hacker/a')
r.recvuntil(b"This program will send you ")
count = int(r.recvuntil(b" ").strip())

for i in range(count):
    r.recvuntil(b'for: ')
    cal = r.recvline().strip().decode()
    cmd = f'python -c "print({cal})"'
    ans = os.popen(cmd).read().strip().encode()
    r.sendline(ans)


r.interactive()



### /home/hacker/a

#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
void pwncollege(){
    printf("pwncollege\n");
}

int main(){
    int pid ;

    pid = fork();

    if(pid == 0){
        execve("/challenge/embryoio_level135",NULL,NULL);
    }else{
        wait(NULL);
        exit(0);
    }
}