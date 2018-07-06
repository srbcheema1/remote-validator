#include <iostream>
#include <fstream>
using namespace std;

int main(){
   ofstream fout;
   fout.open ("bin/out/my_file.txt");
   int i=1;
   while(1) {
       int t;
       cin >> t;
       if(t == 0) break;
       if(t % 2 == 0) fout << "div by 2 , " << i << endl;
       if(t % 7 == 0) fout << "div by 7 , " << i << endl;
       i++;
   }
   fout.close();
   return 0;
}
