// Core-owned slots: FREE, READY, HELD. Consumers never mutate held payloads.
#pragma once
#include "m1_runtime.h"

typedef struct M1Snapshots
{
    M1Snapshot slots[M1_SNAPSHOT_SLOTS];
    uint8_t state[M1_SNAPSHOT_SLOTS];
    uint32_t rejected;
} M1Snapshots;

uint8_t m1_publish(M1Snapshots *pool, const M1Snapshot *value);
uint8_t m1_acquire(M1Snapshots *pool);
void m1_release(M1Snapshots *pool, uint8_t slot);
