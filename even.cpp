#include <iostream>

int main(){
    int t;
    std::cin>>t;
    while(t--){
        int a;
        std::cin >> a;
        if ( a % 2 == 0 ) {
            std::cout << "even" << std::endl;
        } else {
            std::cout << "odd" << std::endl;
        }
    }
    return 0;
}
