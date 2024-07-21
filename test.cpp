#include <iostream>
#include<cstdarg>

using namespace std;

int mult(int f, int s, int t);

int main(){
    cout<< mult(1,2,3);
    return 0;
}

int mult(int f, int s, int t)
{
    int mult_res;
    mult_res = f*s*t;
    return mult_res;
}