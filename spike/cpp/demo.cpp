#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>

using namespace std;

std::vector<char> & readline(std::istream & stream, std::vector<char> & container)
{
    char c;
    container.clear();
    while (stream && stream.get(c)) {
        container.push_back(c);
        if (c == '\n') break;
    }
    return container;
}

int main(){
    ofstream fout;
    fout.open ("bin/out/my_file.txt");
    int i=1;
    int val;

    std::vector<char> line;
    while (readline(std::cin, line).size() != 0) {
        std::string str(line.begin(), line.end());
        std::stringstream sin(str);
        sin >> val;
        if(val == 0) break; // dont use it normally
        if(val % 2 == 0) fout << val << " is div by 2 , " << i << endl;
        if(val % 7 == 0) fout << val << " is div by 7 , " << i << endl;
        i++;
    }

    fout.close();
    return 0;
}
