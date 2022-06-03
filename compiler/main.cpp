#include "UART/UART_due.h"
#include "waitable.h"

UART_due * serial;


extern "C" void putCharacter(char c){ 
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
}
extern "C" void start();

int main( void ){	
   usleep( 1000 );

   UART_due uart;
   serial = &uart;

   start();
}
