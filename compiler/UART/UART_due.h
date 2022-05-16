#ifndef _UART_DUE_H_
#define _UART_DUE_H_

#define __SAM3X8E__
#define register
#include "../include/cortex/atmel/sam.h"
#undef register 

class UART_due {
public:
   UART_due();

   void putc(char c);

   char getc(void);

private:
   Uart *due_uart = UART;
};

#endif // _UART_DUE_H_