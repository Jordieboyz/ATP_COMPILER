#ifndef _WAIT_H_
#define _WAIT_H

#define register
#include "include/cortex/atmel/sam.h"
#include "include/hwlib-arduino-due-system-sam3xa.inc"
#undef register

/// returns the number of ticks since some fixed starting point
uint_fast64_t now_ticks(){
   static bool init_done = false;
   if( ! init_done ){
	   
      // kill the watchdog
      WDT->WDT_MR = WDT_MR_WDDIS;
      
      // switch to the 84 MHz crystal/PLL clock
      sam3xa::SystemInit();
      
      EFC0->EEFC_FMR = EEFC_FMR_FWS(4);
      EFC1->EEFC_FMR = EEFC_FMR_FWS(4);      
      
      SysTick->CTRL  = 0;         // stop the timer
      SysTick->LOAD  = 0xFFFFFF;  // use its as a 24-bit timer
      SysTick->VAL   = 0;         // clear the timer
      SysTick->CTRL  = 5;         // start the timer, 1:1

      init_done = true;      
   }
   
   static unsigned int last_low = 0;
   static unsigned long long int high = 0;

   // the timer ticks down, but we want an up counter
   unsigned int low = 0xFFFFFF - ( SysTick->VAL & 0xFFFFFF );
   if( low < last_low ){
   
      // the timer rolled over, so increment the high part
      high += 0x1ULL << 24;
   }
   last_low = low;

   // return the aggregated ticks value
   // the counter runs at 84 MHz 
   return ( low | high ); 

}   

uint64_t now_us(){
   return now_ticks() / 84;
} 

void usleep( int_fast32_t n ){
   auto end = now_us() + n;
   while( now_us() < end ){}
}


#endif // _WAIT_H