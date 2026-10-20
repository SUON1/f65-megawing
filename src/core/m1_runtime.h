// Development CoreRuntime owns tick, deterministic queue and checksum.
#pragma once
#include "m1_development.h"

typedef struct
{
    M1Command queue[M1_QUEUE_CAPACITY];
    uint32_t tick;
    uint32_t commands;
    uint32_t checksum;
    uint8_t latched_count;
    uint8_t count;
    uint8_t held;
    uint8_t fault;
} M1Core;

void m1_core_init(M1Core *core);
uint8_t m1_command(M1Core *core, M1Command command);
struct M1Snapshots;
void m1_tick(M1Core *core, struct M1Snapshots *pool,
             uint8_t stages[M1_STAGES]);
void m1_extract(const M1Core *core, M1Snapshot *snapshot);
