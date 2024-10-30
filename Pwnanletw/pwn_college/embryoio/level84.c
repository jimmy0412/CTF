#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
void pwncollege(){
    printf("pwncollege\n");
}

int main(){
    int pid, fd ;

    fd = open("ipfavb",O_RDONLY);
    pid = fork();

    if(pid == 0){
        dup2(fd,0);
        close(fd);
        execve("/challenge/embryoio_level84",NULL,NULL);
    }else{
        close(fd);
        wait(NULL);
        printf("child good");
        exit(0);
    }
}

