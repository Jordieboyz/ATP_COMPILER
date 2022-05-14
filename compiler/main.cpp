#include "UART/UART.h"
#include "waitable.h"

DUE_UART * serial;

extern "C" void putCharacter(char c){ serial->putc(c); }
extern "C" void start();

int main( void ){	
   usleep( 10 );

   DUE_UART uart;
   serial = &uart;

   start();
}