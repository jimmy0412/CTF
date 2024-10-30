#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include<fcntl.h>
void pwncollege(){
    printf("pwncollege\n");
}

int main(){
    int pid, fd ;

    pid = fork();

    if(pid == 0){
        execve("/challenge/embryoio_level112",NULL,NULL);
    }else{
        wait(NULL);
        exit(0);
    }
}
