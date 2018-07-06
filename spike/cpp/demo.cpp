#include <iostream>
#include <fstream>
using namespace std;

int main(){
   ofstream fout;
   fout.open ("bin/out/my_file.txt");
   while(1) {
       int t;
       cin >> t;
       if(t == 0) break;
       if(t % 2 == 0) fout << "div by 2" << endl;
       if(t % 7 == 0) fout << "div by 7" << endl;
       cout << t << endl;
   }
   fout.close();
   return 0;
}
