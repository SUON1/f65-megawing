#ifndef R0FC_PLATFORM_H
#define R0FC_PLATFORM_H
#include "combined_model.h"
#define CFREG(a) (*(volatile uint8_t *)(uintptr_t)(a))
extern volatile uint8_t *const cfresult;
extern uint8_t cffault, cfreclaimed;
extern uint32_t cfperiod, cfcia_frame, cfcycles_frame;
extern volatile uint8_t r0f_pf_nmi_seen;
extern volatile uint16_t r0f_pf_irq_count;
void cfput16(uint16_t at,uint16_t v);
void cfput32(uint16_t at,uint32_t v);
uint32_t cfget32(uint16_t at);
void cfadd(uint16_t at,uint32_t v);
uint32_t cfcrc(const volatile uint8_t *p,uint16_t n);
uint8_t cfcopy(uint32_t physical,uint8_t *local,uint8_t n,uint8_t to_chip);
uint32_t cfphysical_crc(uint32_t start,uint32_t bytes);
uint8_t cfentry(void);
uint8_t cfrom_begin(void);
uint8_t cfrom_restore(void);
uint8_t cfclock_begin(void);
uint32_t cfnow(void);
uint32_t cfframe_wait(void);
uint8_t cfcalibrate(uint8_t after);
uint32_t cfcycles(uint32_t counts);
uint32_t cfratio(uint32_t a,uint32_t b,uint32_t denominator,uint8_t shift);
uint8_t cfdma(uint32_t source,uint32_t destination,uint16_t length);
void cfaudio_begin(void);
void cfaudio_service(uint8_t warning);
void cfaudio_stop(void);
void cfinput(void);
void cfinput_tick(uint8_t scripted_state);
void cfexit(void);
void cfscreen(void);
void cffinal_screen(void);
void cfline(uint8_t row,const char *text);
void cfhex(uint8_t row,uint8_t column,uint32_t v,uint8_t digits);
#endif
