#include<stdio.h>
#include<unistd.h>


int main(){
    char *argv[225];
    char *envp[] = {"286=hpcmjsjgep",0};
    for(int i = 0 ; i < 223; i++){
        argv[i] = "eqtvewlchk" ; 
    }
    argv[223] = "eqtvewlchk"; 
    argv[224] = NULL;
    execve("/challenge/embryoio_level71",&argv[0],envp);

    return 0;
}