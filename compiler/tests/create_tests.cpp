
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

struct test {
    uint8_t nth_test = 0;
    std::string inpath;
    std::string out_name;
    int vars[2];
    int n_params;

    test( std::string inpath, std::string out_name) :
        inpath(inpath), 
        out_name(out_name)
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

    char look_for = '?';
    int vars_replaced = 0;
    std::string line;
    while( std::getline(in, line ) ){
        for(unsigned i = 0; i < line.length(); i++){
            if(line[i] == look_for){
                out << get_number(t.vars[vars_replaced]);
                vars_replaced++;
            }
            else {
                out << line[i];
            }
        }
        out << std::endl;
    }
    in.close();
    out.close();

    return 1;
}

int n_tests = 0;


void setup_test( test &t, int p1, int p2 = -1){
    t.nth_test = n_tests++;
    t.n_params = (p2 != -1) + 1;
    t.vars[0] = p1;
    t.vars[1] = p2;
}


int main(){ 

    test _even_odd1( IN_PATH(_even_odd), OUT_NAME(_even_odd));
    setup_test( _even_odd1, 3 );
    create_test(_even_odd1);

    test _even_odd2( IN_PATH(_even_odd), OUT_NAME(_even_odd));
    setup_test( _even_odd2, 6 );
    create_test(_even_odd2);

    test _add_imm( IN_PATH(_add_imm), OUT_NAME(_add_imm));
    setup_test( _add_imm, 3, 7 );
    create_test(_add_imm);

    test _add_imm1( IN_PATH(_add_imm), OUT_NAME(_add_imm));
    setup_test( _add_imm1, 2, 9 );
    create_test(_add_imm1);

    test _add_regs( IN_PATH(_add_regs), OUT_NAME(_add_regs));
    setup_test( _add_regs, 4, 8 );
    create_test(_add_regs);

    test _add_regs1( IN_PATH(_add_regs), OUT_NAME(_add_regs));
    setup_test( _add_regs1, 9, 9 );
    create_test(_add_regs1);

    test _minus_imm( IN_PATH(_minus_imm), OUT_NAME(_minus_imm));
    setup_test( _minus_imm, 23, 4 );
    create_test(_minus_imm);

    test _minus_imm1( IN_PATH(_minus_imm), OUT_NAME(_minus_imm));
    setup_test( _minus_imm1, 15, 11 );
    create_test(_minus_imm1);

    test _minus_regs( IN_PATH(_minus_regs), OUT_NAME(_minus_regs));
    setup_test( _minus_regs, 42, 6 );
    create_test(_minus_regs);
    
    test _minus_regs1( IN_PATH(_minus_regs), OUT_NAME(_minus_regs));
    setup_test( _minus_regs1, 23, 15 );
    create_test(_minus_regs1);

    test _sommig( IN_PATH(_sommig), OUT_NAME(_sommig));
    setup_test( _sommig, 7 );
    create_test(_sommig);

    test _sommig1( IN_PATH(_sommig), OUT_NAME(_sommig));
    setup_test( _sommig1, 17 );
    create_test(_sommig1);

    test _sommig2( IN_PATH(_sommig), OUT_NAME(_sommig));
    setup_test( _sommig2, 24 );
    create_test(_sommig2);
    
    return 0;
}