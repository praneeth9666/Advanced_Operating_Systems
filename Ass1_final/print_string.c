#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(void)
{
    char *s;
    unsigned long int i=1;
    s = strdup("This is my initial string");
     while (i)
     {
          printf("%s\n",s);
          sleep(5);
     }
    return 1;
}
