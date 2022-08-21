#include <stdio.h>
#include <stdlib.h>
int main()
{
int x[4][3],i,j, Ya[4],Yd[4], err, epoch; float net, lr, w[3];
printf("*****Training a Perceptron****** \n ");

printf("Enter the inputs \n");

for(i=0; i<4;i++)
    {
        for(j=0; j<3; j++)
        {
        scanf("%d",&x[i][j]);
        }
    }
printf("Enter the weights associated with each input- \n");
for(i=0; i<3; i++)
    {
        scanf("%f",&w[i]);
    }

printf("Enter the desired output - \n");
for(i=0; i<4; i++)
    {
        scanf("%d", &Yd[i]);
    }
printf("Enter the learning coefficient - \n");
scanf("%f",&lr);
printf("\n");
printf("Bias \t X1 \t X2 \n");
for(i=0; i<4;i++)
    {
        for(j=0; j<3; j++)
        {
                printf("%d\t ",x[i][j]);
        }
        printf("\n");
    }
printf("\n\n\n");

printf("WO \t W1 \t W2 \n");
for(i=0; i<3; i++)
    {
        printf("%.2f \t ",w[i]);
    }
printf("\n\n\n");
printf("Desired output - Yd \n");
for(i=0; i<4; i++)
    {
        printf("%d\n",Yd[i]);
    }
printf("\n\n");
printf("%.2f is the learning coefficient \n\n", lr);
err=0;
epoch=0;
net=0.00;
printf("We \t W1 \t W2 \t NET OUTPUT \t Ya \t Yd \n\n");

do {
    for(i=0; i<4;i++)
    {
        for(j=0; j<3; j++)
        {
            net = net+ (w[j]*x[i][j]);
        }

        if(net>=0)
        {
            Ya[i] = 1;
        }
        else
        {
            Ya[i]=0;
        }
        err=Yd[i]-Ya[i];
        for(j=0; j<3; j++)
            {
                w[j]=w[j]+(lr*x[i][j] *err);
                printf("%.2f \t",w[j]);
            }
        printf("%.2f \t\t %d\t%d \n", net, Ya[i],Yd[i]);
    }
    epoch++;
}while(Ya [0] != Yd[0] || Ya[1] != Yd[1] || Ya[2] != Yd[2] || Ya[3] != Yd[3]);

printf("\nFor learning coefficient %.2f number of epochs is %d \n",lr, epoch);
return 0;
}