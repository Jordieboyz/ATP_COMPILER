#ifndef _WAIT_H_
#define _WAIT_H_

#define register
#include "include/cortex/atmel/sam.h"
#include "include/due-system-sam3xa.inc"
#undef register

// Get the "amount" of ticks so far-ish
uint64_t get_n_ticks(){
	static bool initialized;
	if( ! initialized ){

		// kill the watchdog
      WDT->WDT_MR = WDT_MR_WDDIS;
      
      sam3xa::SystemInit();	         
      
      SysTick->CTRL  = 0;                               // 0; "Pause" the timer
      SysTick->LOAD  = SysTick_LOAD_RELOAD_Msk;   	     // 0xFFFFFF; load a 24 bits timer
      SysTick->VAL   = SysTick_VAL_CURRENT_Msk;         // 0; clear the timer
      SysTick->CTRL  = SysTick_CTRL_CLKSOURCE_Msk |	  // 5; start the timer
               SysTick_CTRL_TICKINT_Msk   |
               SysTick_CTRL_ENABLE_Msk; 
	
		initialized = true;
	}
	
   static uint32_t last_before_rollover = 0;
   static uint64_t n_rollovers = 0; 
   
   uint32_t timer_ticks = SysTick->VAL;

   // Timer counts down, so we should check if the timer rolled back to 0xFFFFFF
   if(timer_ticks > last_before_rollover){
      // Timer rolled over, so increment n_rollovers
      n_rollovers += 1 << 24;
   }
   last_before_rollover = timer_ticks;

   // Timer is counting down, but we count the n_rollovers up, so we need to "reverse" the timer_ticks 
   return ( (0xFFFFFF - (timer_ticks - 0xFFFFFF) ) | n_rollovers );
}

void delay_us( uint32_t us ){
	if(us == 0)
		return;	
	uint64_t start = get_n_ticks();
	while(get_n_ticks() - start < us){}
}

#endif // _WAIT_H