#include<stdio.h>
int main()
{
	//string initialisation
    char Mystr[] = "The puts() function";
    
    int val = puts(Mystr);
    printf("Returned Value Val = %d", val);
    
    return 0;
}
