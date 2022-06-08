#include "UART/UART_due.h"
#include "waitable.h"

UART_due * serial;

extern "C" void putNumber( uint8_t c){ 
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
   serial->putc('\n');
}


// making my life easier to print a whole string of characters
void put_string(const char * str, bool endl = true){
   while( *str )
      serial->putc(*str++);
   if( endl )
      serial->putc('\n');
}

#ifdef UNIT_TESTS 
   #include "include_tests.h"
   
   int passed = 0;
   int failed = 0;

   // C++ implementations and checks for unit tests
   auto cpp_even = [](int b){ return( (int)(b % 2 == 0));};
   auto cpp_add = [](int a, int b){ return( a + b);};
   auto cpp_minus = [](int a, int b){ return( a - b);};
   int cpp_sommig(int n){
      if( n > 1)
         return n + cpp_sommig( n-1 );
      return 1;
   }

   void check_test_one_param( uint8_t p, int (*check)(int), int a ){
      if( p == check(a) )
         passed++;
      else
         failed++;
   };  

   void check_test_two_param( uint8_t p, int (*check2)(int, int), int a, int b ){
      if( p == check2(a, b) )
         passed++;
      else
         failed++;
   }; 

   void perform_tests(){
      #ifdef _t0_even_odd
         check_test_one_param( ((uint8_t )(*t0_even_odd)()), cpp_even, 3); 
      #endif
      #ifdef _t1_even_odd
         check_test_one_param( ((uint8_t )(*t1_even_odd)()), cpp_even, 6); 
      #endif  
      #ifdef _t2_add_imm
         check_test_two_param( ((uint8_t )(*t2_add_imm)()), cpp_add, 3, 7); 
      #endif  
      #ifdef _t3_add_imm
         check_test_two_param( ((uint8_t )(*t3_add_imm)()), cpp_add, 2, 9); 
      #endif 
      #ifdef _t4_add_regs 
         check_test_two_param( ((uint8_t )(*t4_add_regs)()), cpp_add, 4, 8); 
      #endif 
      #ifdef _t5_add_regs
         check_test_two_param( ((uint8_t )(*t5_add_regs)()), cpp_add, 9, 9);
      #endif 
      #ifdef _t6_minus_imm
         check_test_two_param( ((uint8_t )(*t6_minus_imm)()), cpp_minus, 23, 4);
      #endif
      #ifdef _t7_minus_imm
         check_test_two_param( ((uint8_t )(*t7_minus_imm)()), cpp_minus, 15, 11);
      #endif
      #ifdef _t8_minus_regs
         check_test_two_param( ((uint8_t )(*t8_minus_regs)()), cpp_minus, 42, 6);
      #endif
      #ifdef _t9_minus_regs
         check_test_two_param( ((uint8_t )(*t9_minus_regs)()), cpp_minus, 23, 15);
      #endif
      #ifdef _t10_sommig
         check_test_one_param( ((uint8_t )(*t10_sommig)()), cpp_sommig, 7);
      #endif
      #ifdef _t11_sommig
         check_test_one_param( ((uint8_t )(*t11_sommig)()), cpp_sommig, 17);
      #endif
      #ifdef _t12_sommig
         check_test_one_param( ((uint8_t )(*t12_sommig)()), cpp_sommig, 24);
      #endif

      put_string( "Unit test passed succesfully: ", false );
      putNumber( passed );
      put_string( "Unit test failed: ", false );
      putNumber( failed );
   }
#endif


int main( void ){
   
   usleep( 1000 );

   UART_due uart;
   serial = &uart;

   #ifdef UNIT_TESTS 
      perform_tests();
   #endif

   return 1;
}