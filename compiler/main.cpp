#include "UART/UART_due.h"
#include "waitable.h"

// extern "C" const char * create_test(const char * name);

// This is kinda ugly, but ti is the only way for me to properly use the UART::putc in these functions.
UART_due * serial;

// This is the entry point of the program and start label of the asm program.
extern "C" uint8_t start();

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


#define UNIT_TESTS
#ifdef UNIT_TESTS
   #if defined (_even_odd)
      bool perform_test(){
         return (  start() == true);
      }
   #elif defined (_sommig)
      bool perform_test(){
         return ( start() == 45);
      }
   #else
      bool perform_test(){
         const char * no_tests = "No tests were performed!\n";
         while(*no_tests){
            serial->putc(*no_tests++);
         }
         return false;
      }
   #endif
#endif


int main( void ){	
   usleep( 1000 );

   UART_due uart;
   serial = &uart;
   
   if( perform_test() == true ){
      const char * all_tests_passed = "All tests passed succesfully!\n";
      while(*all_tests_passed){
         serial->putc(*all_tests_passed++);
      }
   } else {
      const char * unit_test_failed = "Unit_test_failed!\n";
      while(*unit_test_failed){
         serial->putc(*unit_test_failed++);
      }
   }
   putNumber( start() );
   return 1;
}