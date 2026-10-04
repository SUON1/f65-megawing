// Generated from private r0f_group2_capture_contract.json.
#ifndef R0FG2_CAPTURE_H
#define R0FG2_CAPTURE_H
#include <stdint.h>
#define R0FG2_HEADER_BYTES 28u
#define R0FG2_CRC_AT 348u
#define R0FG2_BLOCK_BYTES 352u
#define R0FG2_UNUSED 165u
#define R0FG2_OBSERVATIONS 2u
#define R0FG2_PAYLOAD_BYTES 12u
#define R0FG2_HARNESS_FAULT 114u
#define R0FG2_O_TICK 0u
#define R0FG2_O_STATUS 2u
#define R0FG2_O_CHECKS 3u
#define R0FG2_O_BEFORE 4u
#define R0FG2_O_AFTER 8u
static const uint8_t r0fg2_identity[] = {71,50,67,49,1,40,8,2,213,93,221,179,47,76,15,39,254,83,249,7,134,50,146,6,1,0,0,0};
extern uint8_t r0fg2_queue_observed[R0FG2_OBSERVATIONS][R0FG2_PAYLOAD_BYTES];
#endif
