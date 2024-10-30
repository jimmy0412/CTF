#include<stdio.h>
#include<unistd.h>


int main(){
    char *envp[]={"26=kwrigkydhd",0};
    execve("/challenge/embryoio_level70",NULL,envp);

    return 0;
}