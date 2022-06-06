
#include <fstream>
#include <vector>

#define SUFFIX .txt
#define STR(x) STR_(x)
#define STR_(x) #x
#define ID(x) x
#define PATH(name, suff) STR(../examples/ID(name)suff)

extern "C" const char * create_test(const char * name);

const char * create_test(const char * name){
    return PATH(name, SUFFIX);
    // static bool init_done;
    // if(init_done){
    //     std::ifstream fs("test_dirs");
    //     if(!fs)
    //         return 0;
        
    //     std::vector<std::string> dirs = {};
    //     std::string line;
    //     while( std::getline(fs, line ) )
    //         dirs.push_back( line );
    //     fs.close();
    //     init_done = true;
    // }

    // std::cout << ;
    // // std::ifstream file(PATH(name));
    // // fs.open(PATH(name));
    // return true;
}

// int main(){

// std::ifstream fs("test_dirs");
//     if(!fs)
//         return 0;
    
//     std::vector<std::string> dirs = {};
//     std::string line;
//     while( std::getline(fs, line ) )
//         dirs.push_back( line );
//     fs.close();


//     // int tests_made = 0;
//     fs.open(dirs[0]);
//     if(!fs){
//         std::cout << "end, not opened\n";
//         return 0;
//     }


//     // int tests_made = 0;
//     fs.open(dirs[0]);
//     if(!fs){
//         std::cout << "end, not opened\n";
//         return 0;
//     }
    







//     for(auto a : dirs){
//         std::cout << a << std::endl;
//     }


//     // int replaced_vars = 0;
//     // while(std::getline(fs, line )){
//     //     for(unsigned i = 0; i <= line.length(); i++){
//     //         #if defined VAR1
            
//     //         if( line[i] == '?' && replaced_vars == 0){
//     //             std::cout << VAR1 << std::endl;
//     //             line[i] = VAR1;
                
//     //             replaced_vars++;
//     //         }
//     //         #if defined VAR2
//     //         if( line[i] == '?' && replaced_vars == 1){
//     //             line[i] = VAR2;
//     //             replaced_vars++;
//     //         }
//     //         #else
//     //             std::cout << replaced_vars << " VARS defined!\n";
//     //         #endif
//     //         #endif
//     //     }
//     //     std::cout << VAR1 << std::endl;
//     //     std::cout<< line << std::endl;
//     //     res += line + '\n';
//     // }
//     // std::cout << res;
//     return 1;
// }
