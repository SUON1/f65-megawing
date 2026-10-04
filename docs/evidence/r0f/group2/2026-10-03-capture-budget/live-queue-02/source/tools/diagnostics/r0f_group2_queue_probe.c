// G2-Q pressure at the actual full stage-13 queue, within both measured epochs.
#include <stdint.h>

#include "combined_model.h"
#include "combined_platform.h"
#include "r0f_group2_capture.h"
#include "successor_lifecycle.h"

uint8_t r0fg2_queue_observed[R0FG2_OBSERVATIONS][R0FG2_PAYLOAD_BYTES];

void r0fg2_queue_live(r0fc_model *model)
{
    static const uint8_t rejected_ids[] = {0u, 9u, 255u};
    uint8_t *out = r0fg2_queue_observed[model->tick == 1u ? 0u : 1u];
    uint8_t saved_rejected = model->rejected;
    uint32_t before = r0fs_crc32((const uint8_t *)model, sizeof(*model));
    out[R0FG2_O_TICK] = (uint8_t)model->tick;
    out[R0FG2_O_TICK + 1u] = (uint8_t)(model->tick >> 8u);
    out[R0FG2_O_STATUS] = 0u;
    out[R0FG2_O_CHECKS] = 0u;
    if (model->event_count != R0FC_QUEUE_CAPACITY)
    {
        out[R0FG2_O_STATUS] = 1u;
    }
    else
    {
        for (uint8_t index = 0u; index < sizeof(rejected_ids); index++)
        {
            if (!r0fc_event(model, rejected_ids[index]) && model->rejected == 1u)
            {
                out[R0FG2_O_CHECKS] |= (uint8_t)(1u << index);
            }
            else
            {
                out[R0FG2_O_STATUS] = 2u;
            }
        }
    }
    // Undo only the fixture's intentionally injected flag. All queue/model
    // bytes must compare equal; the ordinary workload continues unchanged.
    model->rejected = saved_rejected;
    uint32_t after = r0fs_crc32((const uint8_t *)model, sizeof(*model));
    if (after == before)
    {
        out[R0FG2_O_CHECKS] |= 8u;
    }
    else
    {
        out[R0FG2_O_STATUS] = 3u;
    }
    for (uint8_t index = 0u; index < 4u; index++)
    {
        out[R0FG2_O_BEFORE + index] = (uint8_t)(before >> (index * 8u));
        out[R0FG2_O_AFTER + index] = (uint8_t)(after >> (index * 8u));
    }
    if (out[R0FG2_O_STATUS])
    {
        cffault = R0FG2_HARNESS_FAULT;
    }
}
