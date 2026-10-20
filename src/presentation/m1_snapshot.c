#include "m1_snapshot.h"

void m1_extract(const M1Core *core, M1Snapshot *snapshot)
{
    snapshot->tick = core->tick;
    snapshot->commands = core->commands;
    snapshot->checksum = core->checksum;
    snapshot->fault = core->fault;
}

uint8_t m1_publish(M1Snapshots *pool, const M1Snapshot *value)
{
    for (uint8_t i = 0u; i < M1_SNAPSHOT_SLOTS; ++i)
    {
        if (pool->state[i] == 0u)
        {
            pool->slots[i] = *value;
            pool->state[i] = 1u;
            return 1u;
        }
    }
    ++pool->rejected;
    return 0u;
}

uint8_t m1_acquire(M1Snapshots *pool)
{
    uint8_t newest = M1_SNAPSHOT_SLOTS;
    for (uint8_t i = 0u; i < M1_SNAPSHOT_SLOTS; ++i)
    {
        if (pool->state[i] == 1u
            && (newest == M1_SNAPSHOT_SLOTS
                || pool->slots[i].tick > pool->slots[newest].tick))
        {
            newest = i;
        }
    }
    if (newest != M1_SNAPSHOT_SLOTS)
    {
        for (uint8_t i = 0u; i < M1_SNAPSHOT_SLOTS; ++i)
        {
            if (pool->state[i] == 1u)
            {
                pool->state[i] = 0u;
            }
        }
        pool->state[newest] = 2u;
    }
    return newest;
}

void m1_release(M1Snapshots *pool, uint8_t slot)
{
    if (slot < M1_SNAPSHOT_SLOTS && pool->state[slot] == 2u)
    {
        pool->state[slot] = 0u;
    }
}
