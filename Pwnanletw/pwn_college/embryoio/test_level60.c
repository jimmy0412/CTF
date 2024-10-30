// https://www.youtube.com/watch?v=6xbLgZpOBi8

#include<unistd.h>
#include<stdio.h>
#include<stdlib.h>
#include<sys/wait.h>
void pwncollege(){
    printf("pwncollege\n");
}

int main(){
    int pid1, pid2, pipefd[2];
       
    if(pipe(pipefd) == -1)
    {
        fprintf(stderr, "Error creating pipe\n");
        exit(1);
    }

    pid1 = fork();
    if(pid1 < 0 ){
        fprintf(stderr, "Error creating fork\n");
        exit(1);
    }
    if(pid1 == 0){
        dup2(pipefd[0],STDIN_FILENO);
        close(pipefd[0]);
        close(pipefd[1]);
        execlp("cat","cat",NULL);
    }else{
        dup2(pipefd[1],STDOUT_FILENO);
        close(pipefd[0]);
        close(pipefd[1]);
        execlp("/challenge/embryoio_level60","/challenge/embryoio_level60",NULL);
         
    }



    return 0 ;
}