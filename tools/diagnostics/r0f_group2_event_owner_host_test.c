// Exercise the frozen event owner directly; no target or hardware execution.
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "combined_model.h"

#ifdef NDEBUG
#error "Event-owner proof requires assertions"
#endif

// The private event API admits the model's nine command owners.
#define EVENT_OWNER_COUNT (sizeof(((r0fc_model *)0)->command) / sizeof(uint16_t))

static unsigned accepted_cases;
static unsigned rejected_cases;

static void initialize(r0fc_model *model, uint8_t pattern)
{
    // Initialize padding and unused event bytes for whole-object comparisons.
    memset(model, pattern, sizeof(*model));
    r0fc_reset(model);
}

static void accept_event(r0fc_model *model, uint8_t entity)
{
    r0fc_model expected;
    memcpy(&expected, model, sizeof(expected));
    assert(expected.event_count < R0FC_QUEUE_CAPACITY);
    expected.events[expected.event_count] = entity;
    expected.event_count++;
    expected.queue_high = expected.event_count;
    assert(r0fc_event(model, entity) == 1u);
    assert(memcmp(model, &expected, sizeof(expected)) == 0);
    accepted_cases++;
}

static void reject_event(r0fc_model *model, uint8_t entity)
{
    r0fc_model expected;
    memcpy(&expected, model, sizeof(expected));
    expected.rejected = 1u;
    assert(r0fc_event(model, entity) == 0u);
    // Queue contents, count/high-water and all other model bytes must survive.
    assert(memcmp(model, &expected, sizeof(expected)) == 0);
    rejected_cases++;
}

static void full_queue(void)
{
    r0fc_model models[2];
    r0fc_model peer_before;
    initialize(&models[0], 0xa5u);
    initialize(&models[1], 0x5au);
    memcpy(&peer_before, &models[1], sizeof(peer_before));

    for (unsigned index = 0u; index < R0FC_QUEUE_CAPACITY; index++)
    {
        uint8_t entity = (uint8_t)(index % EVENT_OWNER_COUNT);
        accept_event(&models[0], entity);
        assert(models[0].event_count == index + 1u);
        assert(models[0].queue_high == index + 1u);
        for (unsigned queued = 0u; queued <= index; queued++)
        {
            assert(models[0].events[queued] == queued % EVENT_OWNER_COUNT);
        }
    }
    // First one-over latches rejection; subsequent valid owners stay rejected.
    for (unsigned entity = 0u; entity < EVENT_OWNER_COUNT; entity++)
    {
        reject_event(&models[0], (uint8_t)entity);
        assert(memcmp(&models[1], &peer_before, sizeof(peer_before)) == 0);
    }
    r0fc_reset(&models[0]);
    assert(models[0].rejected == 0u && models[0].event_count == 0u);
    assert(models[0].queue_high == 0u);
    accept_event(&models[0], 0u);
    assert(memcmp(&models[1], &peer_before, sizeof(peer_before)) == 0);
    puts("full/one-over: order, flag, sticky rejection, model/peer and reset PASS");
}

static void invalid_owner(void)
{
    const uint8_t invalid[] = {(uint8_t)EVENT_OWNER_COUNT, UINT8_MAX};
    for (unsigned index = 0u; index < sizeof(invalid); index++)
    {
        for (unsigned occupied = 0u; occupied < 2u; occupied++)
        {
            r0fc_model models[2];
            r0fc_model peer_before;
            initialize(&models[0], 0x3cu);
            initialize(&models[1], 0xc3u);
            memcpy(&peer_before, &models[1], sizeof(peer_before));
            if (occupied)
            {
                accept_event(&models[0], 0u);
            }
            assert(models[0].event_count < R0FC_QUEUE_CAPACITY);
            reject_event(&models[0], invalid[index]);
            reject_event(&models[0], invalid[index]);
            assert(memcmp(&models[1], &peer_before, sizeof(peer_before)) == 0);
            r0fc_reset(&models[0]);
            assert(models[0].rejected == 0u && models[0].event_count == 0u);
            assert(models[0].queue_high == 0u);
            accept_event(&models[0], 0u);
            assert(memcmp(&models[1], &peer_before, sizeof(peer_before)) == 0);
        }
    }
    puts("invalid 9/255 at empty/non-full: sticky flag, model/peer and reset PASS");
}

int main(void)
{
    full_queue();
    invalid_owner();
    printf("event-owner PASS: %u accepted, %u rejected calls\n",
           accepted_cases, rejected_cases);
    return 0;
}
