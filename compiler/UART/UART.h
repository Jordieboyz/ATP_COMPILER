#ifndef _UART_H_
#define _UART_H_

#define __SAM3X8E__
#define register
#include "../include/cortex/atmel/sam.h"
#undef register 

class DUE_UART {
public:
   DUE_UART();

   void putc(char c);

   char getc(void);

private:
   Uart *due_uart = UART;
};

#endif // _UART_H_