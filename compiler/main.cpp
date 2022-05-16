#include "UART/UART_due.h"
#include "waitable.h"

UART_due * serial;

extern "C" void putCharacter(char c){ serial->putc(c); }
extern "C" void start();

int main( void ){	
   usleep( 10 );

   UART_due uart;
   serial = &uart;

   start();
}
