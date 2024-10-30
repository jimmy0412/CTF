#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
void pwncollege(){
    printf("pwncollege\n");
}

int main(){
    int pid ;
    char *argv[] = {"/challenge/embryoio_level32","igreyliazh",NULL};  // need to add NULL at the end 
    pid = fork();

    if(pid == 0){
        execve("/challenge/embryoio_level32",argv,NULL);
    }else{
        wait(NULL);
        printf("child good");
        exit(0);
    }
}