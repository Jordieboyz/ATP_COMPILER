#include "UART/UART_due.h"
#include "waitable.h"

// This is kinda ugly, but ti is the only way for me to properly use the UART::putc in these functions.
UART_due * serial;

// This is the entry point of the program and start label of the asm program.
// extern "C" uint8_t start(uint8_t r0, uint8_t r1, uint8_t r2, uint8_t r3);
extern "C" uint16_t start();

// For the right output, we need to turn the char into an integer.
// This is annoying if ( c < 0 && c > 9 ).
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

// C++ implementations and checks for unit tests
auto cpp_even = [](int b){ return( b % 2 == 0);};
auto cpp_add = [](int a, int b){ return( a + b);};
auto cpp_minus = [](int a, int b){ return( a - b);};
int cpp_sommig(int n){
   if( n > 1)
      return n + cpp_sommig( n-1 );
   return 1;
}

#define UNIT_TESTS
#ifdef UNIT_TESTS        
   #if defined (t0_even_odd)
      bool perform_test(){ return ( start() == cpp_even(3)     );} 
   #elif defined (t1_even_odd)
      bool perform_test(){ return ( start() == cpp_even(6)     );}  
   #elif defined (t2_add_imm)
      bool perform_test(){ return ( start() == cpp_add(3, 7)   );}
   #elif defined (t3_add_imm)
      bool perform_test(){ return ( start() == cpp_add(2, 9)   );}
   #elif defined (t4_add_regs)
      bool perform_test(){ return ( start() == cpp_add(4, 8)   );}
   #elif defined (t5_add_regs)
      bool perform_test(){ return ( start() == cpp_add(9, 9)   );}   
   #elif defined (t6_minus_imm)
      bool perform_test(){ return ( start() == cpp_minus(23, 4)   );}
   #elif defined (t7_minus_imm)
      bool perform_test(){ return ( start() == cpp_minus(15, 11)   );}
   #elif defined (t8_minus_regs)
      bool perform_test(){ return ( start() == cpp_minus(42, 6)   );}
   #elif defined (t9_minus_regs)
      bool perform_test(){ return ( start() == cpp_minus(23, 15)   );}   
   #elif defined (t10_sommig)
      bool perform_test(){ return ( start() == cpp_sommig(7)    );}              
   #elif defined (t11_sommig)
      bool perform_test(){ return ( start() == cpp_sommig(17)   );}             
   #elif defined (t12_sommig)
      bool perform_test(){ return ( start() == cpp_sommig(24)  );}             
   #else
      bool perform_test(){ return false; }
   #endif
#endif

int main( void ){
   
   usleep( 1000 );

   UART_due uart;
   serial = &uart;

   #ifdef UNIT_TESTS
      if( perform_test() == true )
         put_string( "Unit test passed succesfully." );
      else 
         put_string( "Unit test failed." );
   #endif

   return 1;
}