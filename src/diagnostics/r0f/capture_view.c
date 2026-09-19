#include <stdint.h>
#include "r0f_interfaces.h"
#ifdef R0F_CAPTURE_TEST
extern volatile uint8_t r0f_host_screen[2000];
#define screen r0f_host_screen
#else
static volatile uint8_t *const screen = (volatile uint8_t *)0x0800;
#endif
extern uint8_t r0f_capture_byte(uint16_t index), r0f_capture_key(void);
extern void r0f_timing_display(void);
static uint32_t stream_crc;
static uint8_t current_page, summary;
_Static_assert(R0F_CAPTURE_PAGE_BYTES == R0F_CAPTURE_ROWS * R0F_CAPTURE_ROW_BYTES, "page layout");
_Static_assert(R0F_CAPTURE_TOTAL_BYTES == R0F_RESULT_BYTES + R0F_RAW_CAPTURE_BYTES, "stream layout");
_Static_assert(R0F_CAPTURE_PAGES == (R0F_CAPTURE_TOTAL_BYTES + R0F_CAPTURE_PAGE_BYTES - 1u) / R0F_CAPTURE_PAGE_BYTES, "page count");

static uint32_t crc(uint16_t start, uint16_t length) {
  uint32_t value = 0xfffffffful;
  while (length--) {
    uint8_t bit;
    value ^= r0f_capture_byte(start++);
    for (bit = 0u; bit != 8u; ++bit)
      value = (value >> 1u) ^ ((value & 1u) ? 0xedb88320ul : 0ul);
  }
  return value ^ 0xfffffffful;
}
static void text(uint8_t row, const char *s) {
  uint16_t p = (uint16_t)row * 80u;
  while (*s) { uint8_t c = (uint8_t)*s++; screen[p++] = c >= 'A' && c <= 'Z' ? (uint8_t)(c & 31u) : c; }
}
static void hex(uint8_t row, uint8_t col, uint32_t value, uint8_t digits) {
  uint16_t p = (uint16_t)row * 80u + col + digits;
  while (digits--) { uint8_t n = (uint8_t)(value & 15u); screen[--p] = n < 10u ? (uint8_t)('0'+n) : (uint8_t)(n-9u); value >>= 4u; }
}
void r0f_capture_render(uint8_t page) {
  uint16_t i, start, length;
  uint8_t row;
  if (page >= R0F_CAPTURE_PAGES) return;
  start = (uint16_t)page * R0F_CAPTURE_PAGE_BYTES;
  length = (uint16_t)(R0F_CAPTURE_TOTAL_BYTES - start);
  if (length > R0F_CAPTURE_PAGE_BYTES) length = R0F_CAPTURE_PAGE_BYTES;
  for (i = 0u; i != 2000u; ++i) screen[i] = 32u;
  text(0u, "R0-F RAW CAPTURE - F65R0F5");
  text(1u, "PAGE 0000 OF 0000 OFFSET 0000 BYTES 0000");
  hex(1u, 5u, (uint16_t)page+1u, 4u); hex(1u, 13u, R0F_CAPTURE_PAGES, 4u);
  hex(1u, 25u, start, 4u); hex(1u, 36u, length, 4u);
  text(2u, "TOTAL 0000 CRC32 00000000 PAGECRC 00000000");
  hex(2u, 6u, R0F_CAPTURE_TOTAL_BYTES, 4u); hex(2u, 17u, stream_crc, 8u);
  hex(2u, 34u, crc(start, length), 8u);
  text(3u, "FIELDS ARE HEX; PAGE COUNT 0016 MEANS 22 PAGES.");
  for (row = 0u; row != R0F_CAPTURE_ROWS; ++row) {
    uint16_t offset = (uint16_t)(start + (uint16_t)row * R0F_CAPTURE_ROW_BYTES);
    uint8_t col;
    hex((uint8_t)(row+4u), 0u, offset, 4u);
    screen[(uint16_t)(row+4u)*80u+4u] = ':';
    for (col = 0u; col != R0F_CAPTURE_ROW_BYTES; ++col) {
      uint16_t at = (uint16_t)(offset+col);
      hex((uint8_t)(row+4u), (uint8_t)(5u+col*2u), at < R0F_CAPTURE_TOTAL_BYTES ? r0f_capture_byte(at) : 0u, 2u);
    }
  }
  text(20u, "RAW CIA COUNTS ONLY - NO CALIBRATED TIME OR R0-F ACCEPTANCE");
  text(21u, r0f_capture_byte(151u) == 127u && r0f_capture_byte(252u) == 0u && r0f_capture_byte(7u) == 127u
       ? "ACQUISITION COMPLETE / INHERITED FUNCTIONAL FIXTURE PASS"
       : "ACQUISITION OR FIXTURE FAILED - DIAGNOSTIC DATA ONLY");
  text(23u, "N/SPACE NEXT   P PREVIOUS   S SUMMARY   C CAPTURE");
  text(24u, "NO DISK WRITES. TIMERS STOPPED. RESET REQUIRED AFTER TEST.");
}
void r0f_capture_init(void) {
  current_page = 0u; summary = 0u;
  stream_crc = crc(0u, R0F_CAPTURE_TOTAL_BYTES);
  r0f_capture_render(current_page);
}
void r0f_capture_command(uint8_t key) {
  if (key >= 'a' && key <= 'z') key = (uint8_t)(key - ('a'-'A'));
  if (key == 'S') { summary = 1u; r0f_timing_display(); return; }
  if (key == 'C') { summary = 0u; r0f_capture_render(current_page); return; }
  if (summary) return;
  if ((key == 'N' || key == ' ') && current_page+1u < R0F_CAPTURE_PAGES) ++current_page;
  else if (key == 'P' && current_page) --current_page;
  else return;
  r0f_capture_render(current_page);
}
void r0f_capture_run(void) {
  r0f_capture_init();
  for (;;) r0f_capture_command(r0f_capture_key());
}
