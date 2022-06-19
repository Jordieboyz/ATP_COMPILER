#include "UART/UART_due.h"
#include "waitable.h"

// A global UART_due instance. 
// This makes calling the UART_due::putc possible witout intializing the UART_due every time
UART_due * serial;

/**
 * @brief
 *  Output a character as an 3 digit integer
 * @details
 *  This functions checks what 'number' we are working with and outputs this 
 *  as an actual integer. 
 *  f.e. c = 13; output: serial->putc('1'); serial->putc('3');
 * 
 * @param c      Given character (which cannot be greater than 3 digits)
 */
extern "C" void put_number(const char c, bool endl = false){ 
   if( c >= 0 && c <= 9){
      serial->putc( c + '0');
   } else if( c >= 10 && c <= 99){
      serial->putc( (c/10) + '0');
      serial->putc( (c - ((c/10)*10)) + '0');
   } else {
      serial->putc( (c/100) + '0');
      serial->putc( (c - (((c/100)*100))) / 10 + '0');
      serial->putc(  c - ((c/100*100)) - (((int)((c - (c/100*100))  /10)) *10) + '0' );
   }
   if( endl )
      serial->putc('\n');
}

/**
 * @brief
 *  Outputs multiple characters in a string.
 * @details
 *  This functions outputs a string using the UART_due::putc().
 *  
 * @param str      String to output
 * @param endl     Bool wether we need an '\n' added at the end of the string.
 */
void put_string(const char * str, bool endl = false){
   while( *str )
      serial->putc(*str++);
   if( endl )
      serial->putc('\n');
}

// #define UNIT_TESTS


/**
 * @brief
 *  Macro wether we need to perform unit tests.
 * @details
 *  This macro is automaticly defined in the @see ../Makefile.inc
 */
#ifdef UNIT_TESTS 
   #define DEBUG
   #include "include_tests.h"
   
   // global variables to keep tracks of the passed or failed tests.
   int passed = 0;
   int failed = 0;

   // C++ implementations of certain functions and checks for unit tests
   auto cpp_even    = [](int a){ return (int)(a % 2 == 0); };
   auto cpp_is      = [](int a, int b){ return b; };
   auto cpp_add     = [](int a, int b){ return a + b; };
   auto cpp_minus   = [](int a, int b){ return a - b; };
   auto cpp_mul     = [](int a, int b){ return a * b; };
   auto cpp_mul_add = [](int a, int b, int exp){ return a + (b * exp); };
   int cpp_sommig(int a){
      if( a > 1)
         return a + cpp_sommig( a - 1 );
      return 1;
   }
   auto cpp_sommig_add = [](int a, int b){return a + cpp_sommig(b);}; 
   auto cpp_sommig_minus = [](int a, int b){return cpp_sommig(b) - a;};


   void get_test_info(int result, int cpp_result){
      put_string("\nExecuted test number: ");
      put_number(passed+failed, true);

      put_string("-> ( ");
      put_number(result);
      put_string(" == ");
      put_number(cpp_result);
      put_string(" )", true);
   }
   /**
    * @brief
    *  Compare two functions with function pointers.
    * @details
    *  This functions compares res with the 
    *  output of fptr. It increments @see passed or @see failed
    *  wether the comparison is equal or not.
    *  
    * @param res      This is the result of the performed '*.asm' routine.
    * @param fptr     This is a function pointer to compare with res.
    * @param a        The first parameter for fptr
    * @param b        The second parameter for fptr
    */
   void check_test( const uint8_t res, int (*fptr)(int), const int a){
      ( res == fptr(a) ) ? passed++: failed++; 
      #ifdef DEBUG
         get_test_info(res, fptr(a));
      #endif
   };

   void check_test( const uint8_t res, int (*fptr)(int, int), 
                                                const int a, const int b ){ 
      ( res == fptr(a, b) ) ? passed++: failed++;
      #ifdef DEBUG
         get_test_info(res, fptr(a, b));
      #endif
   };

   void check_test( const uint8_t res, int (*fptr)(int, int, int), 
                                    const int a, const int b , const int c ){
      ( res == fptr(a, b, c) ) ? passed++: failed++; 
      #ifdef DEBUG
         get_test_info(res, fptr(a, b, c));
      #endif
   };

   /**
    * @brief
    *  Perform unit tests based on preprocessed defenitions;
    * @details
    *  This functions performs tests for the preprocessed defenitions @see ../Makefile.inc.
    *  It performs the @see check_test and uses the '*.asm' function defined in 
    *  @see include_tests.h and the C++ implementations I wrote. After, it outputs @see put_string
    *  The amount of tests passed or failed.
    */
   void perform_tests(){
      #ifdef _t0_even_odd
         check_test( ((uint8_t )(*t0_even_odd)()), cpp_even, 3); 
      #endif
      #ifdef _t1_even_odd
         check_test( ((uint8_t )(*t1_even_odd)()), cpp_even, 6); 
      #endif  
      #ifdef _t2_add_imm
         check_test( ((uint8_t )(*t2_add_imm)()), cpp_add, 3, 7); 
      #endif  
      #ifdef _t3_add_imm
         check_test( ((uint8_t )(*t3_add_imm)()), cpp_add, 2, 9); 
      #endif 
      #ifdef _t4_add_regs 
         check_test( ((uint8_t )(*t4_add_regs)()), cpp_add, 4, 8); 
      #endif 
      #ifdef _t5_add_regs
         check_test( ((uint8_t )(*t5_add_regs)()), cpp_add, 9, 9);
      #endif 
      #ifdef _t6_minus_imm
         check_test( ((uint8_t )(*t6_minus_imm)()), cpp_minus, 23, 4);
      #endif
      #ifdef _t7_minus_imm
         check_test( ((uint8_t )(*t7_minus_imm)()), cpp_minus, 15, 11);
      #endif
      #ifdef _t8_minus_regs
         check_test( ((uint8_t )(*t8_minus_regs)()), cpp_minus, 42, 6);
      #endif
      #ifdef _t9_minus_regs
         check_test( ((uint8_t )(*t9_minus_regs)()), cpp_minus, 23, 15);
      #endif
      #ifdef _t10_sommig
         check_test( ((uint8_t )(*t10_sommig)()), cpp_sommig, 7);
      #endif
      #ifdef _t11_sommig
         check_test( ((uint8_t )(*t11_sommig)()), cpp_sommig, 17);
      #endif
      #ifdef _t12_sommig
         check_test( ((uint8_t )(*t12_sommig)()), cpp_sommig, 24);
      #endif
      #ifdef _t13_mul_regs
         check_test( ((uint8_t )(*t13_mul_regs)()), cpp_mul, 4, 5);
      #endif
      #ifdef t14_mul_regs
         check_test( ((uint8_t )(*t14_mul_regs)()), cpp_mul, 3, 8);
      #endif
      #ifdef _t15_var_is_var
         check_test( ((uint8_t )(*t15_var_is_var)()), cpp_is, 15, 4);
      #endif
      #ifdef _t16_var_is_var
         check_test( ((uint8_t )(*t16_var_is_var)()), cpp_is, 4, 19);
      #endif
      #ifdef _t17_mul_add
         check_test( ((uint8_t )(*t17_mul_add)()), cpp_mul_add, 12, 10, 2);
      #endif
      #ifdef _t18_mul_add
         check_test( ((uint8_t )(*t18_mul_add)()), cpp_mul_add, 19, 3, 3);
      #endif
      #ifdef _t19_sommig_add
         check_test( ((uint8_t )(*t19_sommig_add)()), cpp_sommig_add, 9, 7);
      #endif
      #ifdef _t20_sommig_minus
         check_test( ((uint8_t )(*t20_sommig_minus)()), cpp_sommig_minus, 4, 11);
      #endif

      put_string( "\nUnit test passed succesfully: " );
      put_number( passed, true );
      put_string( "Unit test failed: " );
      put_number( failed, true );
   }
#endif

int main( void ){
   delay_us( 2000 );

   UART_due uart;
   serial = &uart;

   #ifdef UNIT_TESTS 
      perform_tests();
   #endif

   return 1;
}