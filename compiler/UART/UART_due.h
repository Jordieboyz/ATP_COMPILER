#ifndef _UART_DUE_H_
#define _UART_DUE_H_

#define __SAM3X8E__
#define register
#include "../include/cortex/atmel/sam.h"
#undef register 

/*
 * Class for arduino_due-UART implementation
 */ 
class UART_due {
public:
   /*
    * UART_due constructor
    * This constructor initializes the arduino.
    */ 
   UART_due();

   /*
    * Output a single character 
    */ 
   void putc(char c);

private:
   Uart *due_uart = UART;
};

#endif // _UART_DUE_H_