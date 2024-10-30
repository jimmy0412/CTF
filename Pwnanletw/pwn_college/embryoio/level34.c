#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
void pwncollege(){
    printf("pwncollege\n");
}

int main(){
    int pid, fd ;

    fd = open("/tmp/gjwlhu",O_WRONLY);
    pid = fork();

    if(pid == 0){
        dup2(fd,1);
        close(fd);
        execve("/challenge/embryoio_level34",NULL,NULL);
    }else{
        close(fd);
        wait(NULL);
        printf("child good");
        exit(0);
    }
}