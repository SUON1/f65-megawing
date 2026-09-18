#include "resume_model.h"
uint8_t r0fr_transition(uint8_t state, uint8_t event) {
  if(state<R0FR_S_RESUMED && event==state)return (uint8_t)(state+1u);
  return R0FR_S_LOCKOUT;
}
uint8_t r0fr_storage_allowed(uint8_t state,uint8_t restored,uint8_t fault) {
  return (uint8_t)(state==R0FR_S_STORAGE && restored==2u && fault==0u);
}
