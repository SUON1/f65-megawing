#include <stdint.h>
#include "r0f_platform.h"

/* Half-open, subtraction-based bounds avoid both addition overflow and
 * accidental admission of hardware's length-zero meaning (65536 bytes). */
uint8_t r0f_pf_dma_encode(uint8_t *list, uint32_t source, uint32_t dest,
                         uint16_t length) {
  if (!length || length > R0FP_MAX_COPY || source < R0FP_STAGING_START ||
      dest < R0FP_STAGING_START || source >= R0FP_STAGING_END ||
      dest >= R0FP_STAGING_END || length > R0FP_STAGING_END-source ||
      length > R0FP_STAGING_END-dest ||
      (source <= dest ? dest-source < length : source-dest < length)) return 0u;
  list[0]=0x0au; list[1]=0x80u; list[2]=0u;
  list[3]=0x81u; list[4]=0u; list[5]=0u; list[6]=0u;
  list[7]=(uint8_t)length; list[8]=0u;
  list[9]=(uint8_t)source; list[10]=(uint8_t)(source>>8u); list[11]=(uint8_t)(source>>16u);
  list[12]=(uint8_t)dest; list[13]=(uint8_t)(dest>>8u); list[14]=(uint8_t)(dest>>16u);
  list[15]=0u; list[16]=0u;
  return 1u;
}

uint32_t r0f_pf_crc(const volatile uint8_t *bytes, uint16_t length) {
  uint32_t crc=0xffffffffu;
  uint16_t i;
  for (i=0u; i<length; ++i) {
    uint8_t bit;
    crc^=bytes[i];
    for (bit=0u; bit<8u; ++bit) crc=(crc>>1u)^((crc&1u)?0xedb88320u:0u);
  }
  return ~crc;
}
