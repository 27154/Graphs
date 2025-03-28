#include <stdio.h>

int main()
{
    int currency, quarters, dimes, nickels, pennies;
    printf("change owed: ");
    scanf("%d", &currency);

    if(currency < 0)
    {
        printf("Pick a fuckin' integer number yo'Psycho\n");
    }

    quarters = currency/25;
    currency %=25;

    dimes = currency/10;
    currency %=10;

    nickels = currency/5;
    currency %=5;

    pennies = currency;

    printf("Quaerters: %d\n", quarters);
    printf("dimes: %d\n", dimes);
    printf("Nickels: %d\n", nickels);
    printf("Penis:%d", pennies);
}