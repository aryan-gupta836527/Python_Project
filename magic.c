//magic square is a sq matrix such thaat column, diagonal and row sum are equal
// all elements are unique
//elements range from 1 to n^2
#include <stdio.h>
int main() {
    int i, j, row, col, a[10][10], rowsum[10], colsum[10];
    int pd=0, sd=0, k, x=0, b[100];
    printf("Enter dimensions for a:\n");
    scanf("%d %d", &row, &col);
    if (row != col) {
        printf("not square");
        return 0;
    }
    printf("\nEnter elements:\n");
    for (i = 0; i < row; i++) { //i row, j column (m row, n column)
        for (j=0; j < col; j++) {
            scanf("%d", &a[i][j]);
        }
    }
    for (i = 0; i < row; i++) { //copying to 1d
        for (j=0; j<col; j++){
            b[x++] = a[i][j];
        }
    }
    //checking uniqueness
    for (k = 0; k < x-1; k++) {
        for (j=k+1; j<x; j++) {
            if (b[k] == b[j]) {
                printf("Elements are not distinct\nNot magic matrix");
                return 0;
            }
        }
    }
    // finding sum of diagonal
    for (i=0; i < row; i++){
        pd = pd + a[i][i];
    }
    //row sum
    for (i = 0; i < row; i++) {
        rowsum[i] = 0;
        for (j=0; j<col; j++) {
            rowsum[i] = rowsum[i] + a[i][j]; }
        if (rowsum[i] != pd) {
            printf("eNot magic matrix");
            return 0;
        }
    }
    //col sum
    for (i = 0; i < col; i++) {
        colsum[i] = 0;
        for (j=0; j<row; j++) {
            colsum[i] = colsum[i] + a[j][i]; }
        if (colsum[i] != pd) {
            printf("bNot magic matrix");
            return 0;
        }
    }
    //secondary diagonal
    for (i = 0; i < row; i++){
        sd = sd + a[i][row-i-1]; }
    if (sd != pd) {
        printf("dNot a magic matrix\n");
        return 0;
    }
    printf("Given matrix is a magic matrix\n");
    return 0;
}