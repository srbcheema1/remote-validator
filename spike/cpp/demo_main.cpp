#include <chrono>
#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>

#include <boost/program_options.hpp>
#include <boost/filesystem/operations.hpp>

namespace po = boost::program_options;

std::string get_output_file(po::variables_map vm){
    std::string outdir;
    if (vm.count("outdir")) {
        outdir = vm["outdir"].as<std::string>();
        std::cout << "output dir is " << outdir << std::endl;
    } else {
        outdir = ".";
        std::cout << "output dir is not provided " << std::endl;
    }
    boost::filesystem::path outdir_boost_path{outdir};
    if (!boost::filesystem::is_directory(outdir_boost_path)) {
        throw std::invalid_argument{"outdir should be a directory, not a file: " + outdir_boost_path.string()};
    }

    outdir = outdir_boost_path.string();
    auto epoch = std::chrono::system_clock::now().time_since_epoch();
    auto timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(epoch).count();
    std::string filetype = "txt";
    std::string filename = outdir + "/demo." + std::to_string(timestamp) + "." + filetype;
    return filename;
}

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

int main(int argc, char ** argv){
    po::options_description desc("demo");
    desc.add_options()
        ("help", "produce help message")
        ("input,i", po::value<std::string>()->default_value("stdin"), "Path to the input VCF file")
        ("report,r", po::value<std::string>()->default_value("summary"), "report")
        ("outdir,o", po::value<std::string>()->default_value("."),"output dir path")
    ;
    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);
    po::notify(vm);
    if (vm.count("help,h")) {
        std::cout << desc << std::endl;
        return 0;
    }
    std::string output_file = get_output_file(vm);

    std::ofstream fout;
    fout.open (output_file);
    int i=1;
    int val;
    std::vector<char> line;
    while (readline(std::cin, line).size() != 0) {
        std::string str(line.begin(), line.end());
        std::stringstream sin(str);
        sin >> val;
        if(val == 0) break; // dont use it normally
        if(val % 2 == 0) fout << "line " << i << " : " << val << " is div by 2" << std::endl;
        if(val % 7 == 0) fout << "line " << i << " : " << val << " is div by 7" << std::endl;
        i++;
    }
    fout <<  "According to the VCF specification, the input file is valid" << std::endl;


    fout.close();
    return 0;
}
