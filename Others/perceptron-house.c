#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#define a 0.0002 // Set a constant learning rate

// Hypothesis function
float h(int x, float w0, float w1){
    return x*w1+w0;
}

// w0 partial derivative function
float dw0(int *x, int *y, int n, float w0, float w1){
    int i;
    float d = 0;
    for(i=0; i<n; i++){
        d += h(x[i], w0, w1) - y[i];
    }
    return d;
}

// w1 derivative function
float dw1(int *x, int *y, int n, float w0, float w1){
    int i;
    float d = 0;
    for(i=0; i<n; i++){
        d += (h(x[i], w0, w1) - y[i])*x[i];
    }
    return d;
}

float predict(float w0, float w1, int x){
    return (w0 + w1*x);
}

int main(){
    int n = 4, i;
    int x[4] = {64, 80, 63, 100}, y[4] = {200, 250, 195, 300}, new_size;
    float w0, w1, learn_w0, learn_w1, temp0=0, temp1=0;

    printf("Enter the inputs \n");
    for(i=0; i<4; i++)
    {
    scanf("%d",&x[i]);
    }

    printf("Enter the desired outputs \n");
    for(i=0; i<4; i++)
    {
    scanf("%d",&y[i]);
    }

    // Random Weights
    w0 = ((float)rand()/(float)(RAND_MAX));
    w1 = ((float)rand()/(float)(RAND_MAX));

    learn_w0 = dw0(x, y, n, w0, w1);
    learn_w1 = dw1(x, y, n, w0, w1);
    w0 = w0 - a*learn_w0/(float)n;
    w1 = w1 - a*learn_w1/(float)n;
    printf("\n");
    int count=0;
    while( fabs(w0 - temp0) > 0.0001 && fabs(w1 - temp1) > 0.0001 ){
        printf("Epoch: %d - w0: %f w1: %f\n",(count+1), w0, w1);
        temp0 = w0;
        temp1 = w1;
        learn_w0 = dw0(x, y, n, w0, w1);
        learn_w1 = dw1(x, y, n, w0, w1);
        w0 = w0 - a*learn_w0/(float)n;
        w1 = w1 - a*learn_w1/(float)n;
        count++;
    }

    printf("\nweights after convergence\nw0 = %.2f and w1 = %.2f\n", w0, w1);

    printf("\nEnter a house size to predict price : ");
    scanf("%d", &new_size);
    float predicted_price = predict(w0, w1, new_size);

    printf("Price of house with size %d is %.2f\n", new_size, predicted_price);
    return 0;
}