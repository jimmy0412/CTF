#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
void pwncollege(){
    printf("pwncollege\n");
}
int main(){
    int pid ;
    char *envp[] = {"izuogv=sextyjxeqz",0};

    pid = fork();
    
    if(pid == 0){
        execve("/challenge/embryoio_level32",NULL,envp);
    }else{
        wait(NULL);
        printf("child good");
        exit(0);
    }
}