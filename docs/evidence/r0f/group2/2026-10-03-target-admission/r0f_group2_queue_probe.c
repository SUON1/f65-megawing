// Compile-only target admission probe; not an admitted combined-load case.
#include <stdint.h>
#include <string.h>

#include "combined_model.h"
#include "successor_lifecycle.h"

// Private return values, not a serialized result or production fault code.
enum
{
    PROBE_PASS = 0,
    PROBE_PRECONDITION = 1,
    PROBE_ACCEPT = 2,
    PROBE_REJECT = 3,
    PROBE_RESTORE = 4
};

uint8_t r0fg2_queue_probe(r0fc_model *model)
{
    if (model->event_count || model->queue_high || model->rejected)
    {
        return PROBE_PRECONDITION;
    }
    uint8_t saved_events[R0FC_QUEUE_CAPACITY];
    memcpy(saved_events, model->events, sizeof(saved_events));
    uint32_t original = r0fs_crc32((const uint8_t *)model, sizeof(*model));
    uint8_t result = PROBE_PASS;
    for (uint8_t index = 0u; index < R0FC_QUEUE_CAPACITY; index++)
    {
        uint8_t entity = (uint8_t)(index % 9u);
        if (!r0fc_event(model, entity) || model->event_count != index + 1u
            || model->queue_high != index + 1u || model->events[index] != entity)
        {
            result = PROBE_ACCEPT;
            goto restore;
        }
    }
    model->rejected = 1u;
    uint32_t expected = r0fs_crc32((const uint8_t *)model, sizeof(*model));
    model->rejected = 0u;
    for (uint8_t entity = 0u; entity < 9u; entity++)
    {
        if (r0fc_event(model, entity)
            || r0fs_crc32((const uint8_t *)model, sizeof(*model)) != expected)
        {
            result = PROBE_REJECT;
            goto restore;
        }
    }
restore:
    memcpy(model->events, saved_events, sizeof(saved_events));
    model->event_count = 0u;
    model->queue_high = 0u;
    model->rejected = 0u;
    if (r0fs_crc32((const uint8_t *)model, sizeof(*model)) != original)
    {
        return PROBE_RESTORE;
    }
    return result;
}
