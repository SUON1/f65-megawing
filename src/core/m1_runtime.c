#include <string.h>

#include "m1_runtime.h"
#include "m1_snapshot.h"

void m1_core_init(M1Core *core)
{
    memset(core, 0, sizeof(*core));
    core->checksum = 0x65a001u;
}

uint8_t m1_command(M1Core *core, M1Command command)
{
    if (core->count == M1_QUEUE_CAPACITY || command.tick <= core->tick
        || (command.pressed & command.released) != 0u
        || ((command.pressed | command.released) & 0xfeu) != 0u
        || (core->count != 0u && command.tick < core->queue[core->count - 1u].tick))
    {
        core->fault |= 1u;
        return 0u;
    }
    core->queue[core->count++] = command;
    return 1u;
}

void m1_tick(M1Core *core, M1Snapshots *pool, uint8_t stages[M1_STAGES])
{
    if (core->tick == UINT32_MAX)
    {
        core->fault |= 2u;
        return;
    }
    M1Snapshot snapshot;
    for (uint8_t stage = 1u; stage <= M1_STAGES; ++stage)
    {
        stages[stage - 1u] = stage;
        if (stage == 1u)
        {
            ++core->tick;
        }
        else if (stage == 2u)
        {
            // Freeze this tick's eligible semantic batch before applying it.
            core->latched_count = 0u;
            while (core->latched_count < core->count
                   && core->queue[core->latched_count].tick <= core->tick)
            {
                ++core->latched_count;
            }
        }
        else if (stage == 3u)
        {
            while (core->latched_count != 0u)
            {
                M1Command command = core->queue[0];
                core->held = (uint8_t)((core->held | command.pressed)
                             & (uint8_t)~command.released);
                ++core->commands;
                --core->count;
                --core->latched_count;
                for (uint8_t i = 0u; i < core->count; ++i)
                {
                    core->queue[i] = core->queue[i + 1u];
                }
            }
        }
        else if (stage == 19u)
        {
            m1_extract(core, &snapshot);
        }
        else if (stage == 20u)
        {
            // Explicit values, never native struct padding or presentation state.
            uint32_t hash = core->checksum;
            hash = (hash << 5u) | (hash >> 27u);
            core->checksum = hash ^ core->tick ^ core->commands
                             ^ core->held ^ core->fault;
            // Future semantic commands are authoritative; hash fields in order.
            for (uint8_t i = 0u; i < core->count; ++i)
            {
                uint32_t queued = core->queue[i].tick
                                  ^ ((uint32_t)core->queue[i].pressed << 24u)
                                  ^ ((uint32_t)core->queue[i].released << 16u);
                core->checksum = (core->checksum << 5u)
                                 | (core->checksum >> 27u);
                core->checksum ^= queued;
            }
        }
        else if (stage == 21u)
        {
            snapshot.checksum = core->checksum;
            (void)m1_publish(pool, &snapshot);
        }
        // Unimplemented owners remain explicit disabled stage slots.
    }
}
