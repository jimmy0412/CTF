#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
void pwncollege(){
    printf("pwncollege\n");
}

int main(){
    int pid ;
    
    pid = fork();
    chdir("/tmp/imufsx");
    if(pid == 0){
        execve("/challenge/embryoio_level32",NULL,NULL);
    }else{
        wait(NULL);
        exit(0);
    }
}