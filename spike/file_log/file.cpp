#include<iostream>
#include<fstream>
using namespace std;

int main()
{
   ofstream ofile;
   ofile.open ("my_file.txt");
   ofile << "geeksforgeeks" << endl;
   ofile << "geeksforgeeks" << endl;

   int t;
   cin>>t;
   while(t--){
       string inp;
       cin >> inp;
       ofile << inp << endl;
   }

   ofile.close();
   return 0;
}
