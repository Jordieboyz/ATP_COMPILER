#ifndef _CONN_
#define _CONN_

#include <fstream>

#define SUFFIX .txt
#define TSUFFIX .tst

#define STR(x) STR_(x)
#define STR_(x) #x
#define ID(x) x
#define IN_PATH(name, suff) STR(../examples/templates/ID(name)suff)
#define OUT_NAME(name, suff) STR(ID(name)suff)

struct test {
    uint8_t nth_test = 0;
    std::string inpath;
    std::string out_name;
    uint8_t var1 = -1;
    uint8_t var2 = -1;
    
    test( uint8_t n, std::string inpath, std::string out_name, uint8_t var1) :
        nth_test(n),
        inpath(inpath), 
        out_name(out_name), 
        var1(var1) 
    {}

    test( uint8_t n, std::string inpath, std::string out_name, uint8_t var1, uint8_t var2) : 
        nth_test(n), 
        inpath(inpath), 
        out_name(out_name), 
        var1(var1), 
        var2(var2) 
    {}
};

std::string get_number(uint8_t c){
    std::string number;
    if( c >= 0 && c <= 9){
        number += (c + '0');
    } else if( c >= 10 && c <= 99){
        number += ( (c/10) + '0');
        number += ( (c - ((c/10)*10)) + '0');
    } else {
        number += ( (c/100) + '0');
        number += ( (c - (((c/100)*100))) / 10 + '0');
        number += (  c - ((c/100*100)) - (((int)((c - (c/100*100))  /10)) *10) + '0' );
    }
    return number;
}


bool create_test(test &t){
    std::string out_name = get_number(t.nth_test) + t.out_name;
    std::fstream out( "tests/t"+out_name , std::fstream::out);
    if(!out)
        return 0;

    std::fstream in(t.inpath, std::fstream::in);
    if(!in)
        return 0;

    int vars_replaced = 0;
    std::string line;
    while( std::getline(in, line ) ){
        for(unsigned i = 0; i < line.length(); i++){
            if(line[i] == '?' && vars_replaced == 0 && t.var1 != -1){
                out << get_number(t.var1);
                vars_replaced++;
            }
            else if(line[i] == '?' && vars_replaced == 1 && t.var2 != -1){
                out << get_number(t.var2);
                vars_replaced++;
            }
            else{
                out << line[i];
            }
        }
        out << std::endl;
    }
    in.close();
    out.close();

    return 1;
}

int main(){ 
    int n_tests = 0;

    test _even_odd1( n_tests, IN_PATH(_even_odd, SUFFIX), OUT_NAME(_even_odd, TSUFFIX), 3 );  
    create_test(_even_odd1);
    n_tests++;

    test _even_odd2( n_tests, IN_PATH(_even_odd, SUFFIX), OUT_NAME(_even_odd, TSUFFIX), 6 );  
    create_test(_even_odd2);
    n_tests++;

    test _add_imm1( n_tests, IN_PATH(_add_imm, SUFFIX), OUT_NAME(_add_imm, TSUFFIX), 3, 7 );  
    create_test(_add_imm1);
    n_tests++;

    test _add_imm2( n_tests, IN_PATH(_add_imm, SUFFIX), OUT_NAME(_add_imm, TSUFFIX), 2, 9 );  
    create_test(_add_imm2);
    n_tests++;

    test _add_regs1( n_tests, IN_PATH(_add_regs, SUFFIX), OUT_NAME(_add_regs, TSUFFIX), 8, 4 );  
    create_test(_add_regs1);
    n_tests++;

    test _add_regs2( n_tests, IN_PATH(_add_regs, SUFFIX), OUT_NAME(_add_regs, TSUFFIX), 9, 9 );  
    create_test(_add_regs2);
    n_tests++;

    test _minus_imm1( n_tests, IN_PATH(_minus_imm, SUFFIX), OUT_NAME(_minus_imm, TSUFFIX), 23, 4 );
    create_test(_minus_imm1);
    n_tests++;

    test _minus_imm2( n_tests, IN_PATH(_minus_imm, SUFFIX), OUT_NAME(_minus_imm, TSUFFIX), 15, 11 );  
    create_test(_minus_imm2);
    n_tests++;

    test _minus_regs1( n_tests, IN_PATH(_minus_regs, SUFFIX), OUT_NAME(_minus_regs, TSUFFIX), 42, 6 );  
    create_test(_minus_regs1);
    n_tests++;

    test _minus_regs2( n_tests, IN_PATH(_minus_regs, SUFFIX), OUT_NAME(_minus_regs, TSUFFIX), 23, 15 );  
    create_test(_minus_regs2);
    n_tests++;

    test _sommig( n_tests, IN_PATH(_sommig, SUFFIX), OUT_NAME(_sommig, TSUFFIX) , 7 );  
    create_test(_sommig);
    n_tests++;

    test _sommig2( n_tests, IN_PATH(_sommig, SUFFIX),  OUT_NAME(_sommig, TSUFFIX), 17 );  
    create_test(_sommig2);
    n_tests++;

    test _sommig3( n_tests, IN_PATH(_sommig, SUFFIX), OUT_NAME(_sommig, TSUFFIX), 24 );  
    create_test(_sommig3);
    n_tests++;

    return 0;
}


#endif