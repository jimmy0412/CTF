#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
void pwncollege(){
    printf("pwncollege\n");
}

int main(){
    int pid ;
    char *argv[183];

    for(int i = 0 ; i < 181 ; i++){
        argv[i] = "yugfnmqhnp" ; 
    }
    argv[181] = "yugfnmqhnp";
    argv[182] = NULL;

    pid = fork();

    if(pid == 0){
        execve("/challenge/embryoio_level80",argv,NULL);
    }else{
        wait(NULL);
        exit(0);
    }
}