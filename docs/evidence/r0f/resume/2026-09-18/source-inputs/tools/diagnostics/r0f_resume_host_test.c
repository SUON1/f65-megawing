#include <assert.h>
#include <stdio.h>
#include "resume_model.h"
int main(void) {
  unsigned s,e,r,f;unsigned checks=0u;
  for(s=0u;s<256u;++s)for(e=0u;e<256u;++e) {
    uint8_t expected=R0FR_S_LOCKOUT;
    if(s<5u&&e==s)expected=(uint8_t)(s+1u);
    assert(r0fr_transition((uint8_t)s,(uint8_t)e)==expected);++checks;
  }
  for(s=0u;s<256u;++s)for(r=0u;r<256u;++r)for(f=0u;f<256u;++f) {
    assert(r0fr_storage_allowed((uint8_t)s,(uint8_t)r,(uint8_t)f)==(s==4u&&r==2u&&f==0u));++checks;
  }
  printf("RH001 admission/invalid-state/lockout checks PASS: %u\n",checks);
  return 0;
}
