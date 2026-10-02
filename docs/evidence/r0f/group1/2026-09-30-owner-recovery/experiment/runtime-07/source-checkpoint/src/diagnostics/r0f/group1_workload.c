#include <stdint.h>

#include "combined_model.h"
#include "group1_workload.h"
#include "group1_pool_owners.h"
#include "r0f_group1_trace.h"

// Distinct state for six full-shape and three reduced-shape aircraft fixtures,
// two isolated knowledge domains and next-tick held intentions. No renderer,
// storage or hardware dependency. Counts are owned by the private contract.
static uint16_t full[R0FG1_SIX_DOF][6];
static uint16_t reduced[R0FG1_KINEMATIC][3];
static uint16_t tracks[R0FG1_DOMAINS][R0FG1_TRACKS_PER_DOMAIN];
static uint8_t populated[R0FG1_DOMAINS];
static uint16_t intent[9], pending[9], eligible[9];
static uint16_t runs[3], causality_errors;

void r0fg1_workload_stage(uint8_t stage, uint16_t tick)
{
    if (stage == 3u)
    {
        for (uint8_t actor = 0u; actor < 9u; actor++)
        {
            if (eligible[actor] != 0u && tick >= eligible[actor])
            {
                if (tick != eligible[actor])
                {
                    causality_errors++;
                }
                intent[actor] = pending[actor];
                eligible[actor] = 0u;
            }
        }
    }
    else if (stage == 8u)
    {
        for (uint8_t actor = 0u; actor < R0FG1_SIX_DOF; actor++)
        {
            for (uint8_t axis = 0u; axis < 6u; axis++)
            {
                full[actor][axis] = (uint16_t)(full[actor][axis]
                    + intent[actor] + tick + axis + actor);
            }
        }
        for (uint8_t actor = 0u; actor < R0FG1_KINEMATIC; actor++)
        {
            for (uint8_t axis = 0u; axis < 3u; axis++)
            {
                reduced[actor][axis] = (uint16_t)(reduced[actor][axis]
                    + intent[actor + R0FG1_SIX_DOF] + tick + axis);
            }
        }
    }
    else if (stage == 15u)
    {
        for (uint8_t domain = 0u; domain < R0FG1_DOMAINS; domain++)
        {
            for (uint8_t track = 0u; track < R0FG1_TRACKS_PER_DOMAIN; track++)
            {
                // Independent domain input stream. No other domain read.
                tracks[domain][track] = (uint16_t)(tracks[domain][track]
                    + tick + (uint16_t)(domain * 37u) + track + 1u);
                if (populated[domain] <= track)
                {
                    populated[domain]++;
                    r0fg1_owner_sample((uint8_t)(R0FG1_POOL_MEGA_TRACKS + domain),
                                       populated[domain]);
                }
            }
            r0fg1_owner_sample((uint8_t)(R0FG1_POOL_MEGA_TRACKS + domain),
                               populated[domain]);
        }
    }
    else if (stage == 16u)
    {
        // Diagnostic due-pattern corpus, not approved production AI cadences.
        static const uint8_t cadence[3] = {2u, 5u, 10u};
        for (uint8_t tier = 0u; tier < 3u; tier++)
        {
            if (tick % cadence[tier] != 0u)
            {
                continue;
            }
            runs[tier]++;
            for (uint8_t actor = tier; actor < 9u; actor = (uint8_t)(actor + 3u))
            {
                uint8_t domain = actor < 5u ? 0u : 1u;
                pending[actor] = tracks[domain][actor];
                eligible[actor] = (uint16_t)(tick + 1u);
            }
        }
    }
}

uint32_t r0fg1_workload_hash(void)
{
    uint32_t hash = 0x47315731ul;
    for (uint8_t actor = 0u; actor < R0FG1_SIX_DOF; actor++)
    {
        for (uint8_t axis = 0u; axis < 6u; axis++)
        {
            hash = r0fc_hash(hash, full[actor][axis]);
        }
    }
    for (uint8_t actor = 0u; actor < R0FG1_KINEMATIC; actor++)
    {
        for (uint8_t axis = 0u; axis < 3u; axis++)
        {
            hash = r0fc_hash(hash, reduced[actor][axis]);
        }
    }
    for (uint8_t domain = 0u; domain < R0FG1_DOMAINS; domain++)
    {
        for (uint8_t track = 0u; track < R0FG1_TRACKS_PER_DOMAIN; track++)
        {
            hash = r0fc_hash(hash, tracks[domain][track]);
        }
    }
    for (uint8_t actor = 0u; actor < 9u; actor++)
    {
        hash = r0fc_hash(r0fc_hash(r0fc_hash(hash, intent[actor]),
                                 pending[actor]), eligible[actor]);
    }
    return hash;
}

uint16_t r0fg1_ai_runs(uint8_t tier)
{
    return tier < 3u ? runs[tier] : 0u;
}

uint16_t r0fg1_causality_errors(void)
{
    return causality_errors;
}
