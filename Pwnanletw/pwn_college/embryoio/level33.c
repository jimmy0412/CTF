#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include <fcntl.h>
void pwncollege(){
    printf("pwncollege\n");
}
int main(){
    int pid , fd;

    fd = open("/tmp/dqwzmk",O_RDONLY);
    pid = fork();
    
    if(pid == 0){
        dup2(fd,0);  // redirect stdin to our file
        close(fd);
        execve("/challenge/embryoio_level33",NULL,NULL);

    }else{
        close(fd);
        wait(NULL);
        printf("child good");
        exit(0);
    }
}