#include<linux/module.h>
#include<linux/kernel.h>
#include<linux/cred.h>
#include<linux/sched.h>
MODULE_LICENSE("GPL");


void *test(void){
    printk("%d",MSR_GS_BASE);
    return 0 ;
}


void test2(void){
    printk("%ld",current->thread_info.flags);
}
void test3(void){
    current->thread_info.flags &= ~(1 << TIF_SECCOMP);
}

int init_module(void){
printk(KERN_INFO"CURRENT : %p",&current->thread_info);
printk(KERN_INFO"FLAG BEFORE : %ld\n",current->thread_info.flags);
current->thread_info.flags &= ~(1 << TIF_SECCOMP);
printk(KERN_INFO"FLAG AFTER : %ld\n",current->thread_info.flags);
return 0;
}

void cleanup_module(void){
    printk(KERN_INFO"QQQQQ\n");
}