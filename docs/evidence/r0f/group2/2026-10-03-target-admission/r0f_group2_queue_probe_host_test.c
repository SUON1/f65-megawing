// Verify the admission probe leaves both model objects byte-identical.
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "combined_model.h"

uint8_t r0fg2_queue_probe(r0fc_model *model);

int main(void)
{
    r0fc_model models[2];
    r0fc_model before[2];
    memset(models, 0xa5, sizeof(models));
    r0fc_reset(&models[0]);
    r0fc_reset(&models[1]);
    memcpy(before, models, sizeof(before));
    assert(r0fg2_queue_probe(&models[0]) == 0u);
    assert(memcmp(before, models, sizeof(before)) == 0);
    models[0].event_count = 1u;
    memcpy(before, models, sizeof(before));
    assert(r0fg2_queue_probe(&models[0]) == 1u);
    assert(memcmp(before, models, sizeof(before)) == 0);
    puts("Queue admission probe: actual owner, restoration and precondition PASS");
    return 0;
}
