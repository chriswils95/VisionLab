#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

int main(){
uint32_t a = 0b1;
int b = ~a;
b = abs(b);
printf("b is %d\n\r", b);
}