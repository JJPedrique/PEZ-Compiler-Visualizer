#include<iostream>
using namespace std;

void TablaMultiplicar(int n){
    for(int i = 0; i <= 10; i++){
        int Mult = i*n;
        cout<<n<<" x "<<i<<" = "<<Mult<<endl;
    }
}

int main(){
    TablaMultiplicar(2);
}
