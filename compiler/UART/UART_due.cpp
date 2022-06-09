#include "UART_due.h"

UART_due::UART_due(){
    // enable the clock to port A
    PMC->PMC_PCER0 = 1 << ID_PIOA;
    
    // disable PIO Control on PA9 and set up for Peripheral A
    PIOA->PIO_PDR   = PIO_PA8; 
    PIOA->PIO_ABSR &= ~PIO_PA8; 
    PIOA->PIO_PDR   = PIO_PA9; 
    PIOA->PIO_ABSR &= ~PIO_PA9; 

    // enable the clock to the UART
    PMC->PMC_PCER0 = ( 0x01 << ID_UART );

    // Reset and disable receiver and transmitter.
    due_uart->UART_CR = UART_CR_RSTTX | UART_CR_TXDIS;

    // Set the baudrate to 115200.
    due_uart->UART_BRGR = 5241600 / 115200; 

    // No parity, normal channel mode.
    due_uart->UART_MR = UART_MR_PAR_NO;

    // Disable all interrupts.	  
    due_uart->UART_IDR = 0xFFFFFFFF;   

    // Enable the receiver and the trasmitter.
    due_uart->UART_CR = UART_CR_TXEN;
}

void UART_due::putc(char c){
    // wait until no character has been written to UART_THR (or not yet transferred to the Shift Register)
    while((due_uart->UART_SR & UART_SR_TXRDY) == 0){};
    due_uart->UART_THR = c;
}