#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
   int val;
   char str[20];
   
   strcpy(str, "98993489");
   val = atoi(str);
   printf("String value = %s, Int value = %d\n", str, val);

   strcpy(str, "\x61\x33\x00");
   val = atoi(str);
   printf("String value = %s, Int value = %d", str, val);

   return(0);
}
