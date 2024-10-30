#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/stat.h>

// execute "bash 1.sh" at /tmp
int main(){

    int pid ;
    chdir("/tmp/zgtfuj");
    execlp("/challenge/embryoio_level73","/challenge/embryoio_level73",NULL);

    return 0;
}