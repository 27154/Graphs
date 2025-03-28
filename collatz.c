#include <stdio.h>

int main(void)
{
    long long number;
    printf("Pick a number: ");
    scanf("%lld", &number);
    printf("%lld ", number);
    
    while(number !=1)
    {
        if( number % 2 == 0)
        {
            number/=2;
        }
        else
        {
            number = (number * 3) + 1;
        }
        
        printf("%lld  ", number);
    }
    return 0;
}