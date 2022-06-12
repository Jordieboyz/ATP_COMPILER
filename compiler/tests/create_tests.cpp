
#include <fstream>

// user defined macro's
#define TEMPLATEPATH ../templates
#define TEMPLATESUFF .txt
#define TESTSUFF .tst

// program defined macro's
#define STR(x) STR_(x)
#define STR_(x) #x
#define ID(x) x
#define IN_PATH(name) STR(TEMPLATEPATH/ID(name)TEMPLATESUFF)
#define OUT_NAME(name) STR(ID(name)TESTSUFF)

/**
 * @brief
 *  Struct with parameter for unit tests.
 * @details
 *  This @struct holds the parameters for unit tests.
 * 
 * @param nthTest       The number of produced test of the program
 * @param inPath        The absolute path to the 'template file'
 * @param outName       Name of the output file
 * @param vars          This holds the 1 or 2 template variables (depending on template)
 * @param nVars         Amount of variables in @param vars
 */
struct Test {
    int nthTest = 0;
    std::string inPath;
    std::string outName;
    int vars[3];
    int nVars;

    Test( std::string inPath, std::string outName ) :
        inPath(inPath), 
        outName(outName)
    {}
};

// global variable to keep track of the amount of created tests
int nTests = 0;

/**
 * @brief
 *  A fucntion to create unit tests.
 * @details
 *  This function will create and output a test file based on a template.
 *  It sets up the @see @struct Test with f.e. it's parameters. After, it 
 *  reads the input file character for character and replaces the '?' with vars;
 * 
 * @param t             Reference to a @struct Test
 * @param var1          The first parameter for the @struct Test::vars
 * @param var2          The second parameter for the @struct Test::vars
 */
void create_test(Test &t, int var1, int var2 = -1, int var3 = -1){
    // setup for the creation of the test
    t.nthTest = nTests++;
    t.nVars = (var3 == -1) ? (var2 == -1) ? 2 : 1: 3;
    t.vars[0] = var1;
    t.vars[1] = var2;
    t.vars[2] = var3;


    // fstream for input and output files
    std::fstream in(t.inPath, std::fstream::in);
    std::fstream out( "tests/t" + std::to_string(t.nthTest) + t.outName , 
                                                            std::fstream::out);
    if(!in | !out)
        return;

    // read inputfile char by char and replace the placeholder '?' with test::vars
    char byte = 0;
    int varsReplaced = 0;

    while( in.get( byte ) )
        (byte == '?') ? 
                out << std::to_string(t.vars[varsReplaced++]) :
                out << byte;
         
    in.close();
    out.close();
}





int main(){ 



    Test _even_odd1( IN_PATH(_even_odd), OUT_NAME(_even_odd));
    create_test(_even_odd1, 3 );

    Test _even_odd2( IN_PATH(_even_odd), OUT_NAME(_even_odd));
    create_test( _even_odd2, 6 );

    Test _add_imm( IN_PATH(_add_imm), OUT_NAME(_add_imm));
    create_test( _add_imm, 3, 7 );

    Test _add_imm1( IN_PATH(_add_imm), OUT_NAME(_add_imm));
    create_test( _add_imm1, 2, 9 );

    Test _add_regs( IN_PATH(_add_regs), OUT_NAME(_add_regs));
    create_test( _add_regs, 4, 8 );

    Test _add_regs1( IN_PATH(_add_regs), OUT_NAME(_add_regs));
    create_test( _add_regs1, 9, 9 );

    Test _minus_imm( IN_PATH(_minus_imm), OUT_NAME(_minus_imm));
    create_test( _minus_imm, 23, 4 );

    Test _minus_imm1( IN_PATH(_minus_imm), OUT_NAME(_minus_imm));
    create_test( _minus_imm1, 15, 11 );

    Test _minus_regs( IN_PATH(_minus_regs), OUT_NAME(_minus_regs));
    create_test( _minus_regs, 42, 6 );
    
    Test _minus_regs1( IN_PATH(_minus_regs), OUT_NAME(_minus_regs));
    create_test( _minus_regs1, 23, 15 );

    Test _sommig( IN_PATH(_sommig), OUT_NAME(_sommig));
    create_test( _sommig, 7 );

    Test _sommig1( IN_PATH(_sommig), OUT_NAME(_sommig));
    create_test( _sommig1, 17 );

    Test _sommig2( IN_PATH(_sommig), OUT_NAME(_sommig));
    create_test( _sommig2, 24 );
    
    Test _mul_regs( IN_PATH(_mul_regs), OUT_NAME(_mul_regs));
    create_test( _mul_regs, 4, 5 );

    Test _mul_regs1( IN_PATH(_mul_regs), OUT_NAME(_mul_regs));
    create_test( _mul_regs1, 3, 8 );

    Test _var_is_var( IN_PATH(_var_is_var), OUT_NAME(_var_is_var));
    create_test( _var_is_var, 15, 4 );

    Test _var_is_var1( IN_PATH(_var_is_var), OUT_NAME(_var_is_var));
    create_test( _var_is_var1, 4, 19 );

    Test _mul_add( IN_PATH(_mul_add), OUT_NAME(_mul_add));
    create_test( _mul_add, 12, 10, 2 );

    Test _mul_add1( IN_PATH(_mul_add), OUT_NAME(_mul_add));
    create_test( _mul_add1, 19, 3, 3 );

    Test _sommig_add( IN_PATH(_sommig_add), OUT_NAME(_sommig_add));
    create_test( _sommig_add, 9, 7 );

    Test _sommig_minus( IN_PATH(_sommig_minus), OUT_NAME(_sommig_minus));
    create_test( _sommig_minus, 4, 11 );

    return 0;
}